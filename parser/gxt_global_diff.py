#!/usr/bin/env python3
import argparse, io, os, re, sys
from typing import Dict, List, Tuple

# ---------- parsing helpers (same behaviour as before) ----------
PAIR_RE   = re.compile(r"^\s*(0x[0-9A-Fa-f]+)\s*=\s*(.*)$")
OPEN_BRACE_RE  = re.compile(r"{\s*$")
CLOSE_BRACE_RE = re.compile(r"}\s*$")
COMMENT_PREFIXES = ("#", ";", "//")

def smart_read(path: str, encodings=("utf-8-sig","utf-16","utf-16le","utf-16be","cp1252")) -> str:
    last = None
    for enc in encodings:
        try:
            with io.open(path, "r", encoding=enc) as f:
                return f.read()
        except Exception as e:
            last = e
    with io.open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        sys.stderr.write(f"[warn] Decoding {path} lossily ({last}).\n")
        return f.read()

def is_comment_or_blank(s: str) -> bool:
    t = s.strip()
    if not t: return True
    return any(t.startswith(p) for p in COMMENT_PREFIXES)

def parse_global_text(text: str) -> Tuple[Dict[str,str], List[str]]:
    in_block = False
    d: Dict[str, str] = {}
    order: List[str] = []
    for line in text.splitlines():
        if not in_block:
            if OPEN_BRACE_RE.search(line):
                in_block = True
            continue
        if CLOSE_BRACE_RE.search(line):
            break
        if is_comment_or_blank(line):
            continue
        m = PAIR_RE.match(line)
        if not m:
            continue
        key, val = m.group(1), m.group(2)
        if key not in d:
            d[key] = val
            order.append(key)
        else:
            d[key] = val
    return d, order

def parse_global_file(path: str) -> Tuple[Dict[str,str], List[str]]:
    return parse_global_text(smart_read(path))

def emit_lines(keys: List[str], src: Dict[str,str], indent="\t") -> List[str]:
    return [f"{indent}{k} = {src.get(k,'')}" for k in keys]

def write_output(path: str, lines: List[str], wrap: bool, title: str, indent="\t"):
    with io.open(path, "w", encoding="utf-8") as f:
        if wrap:
            f.write(f"Version 2 30{('  # ' + title) if title else ''}\n")
            f.write("{\n")
            for L in lines:
                f.write(L + "\n")
            f.write("}\n")
        else:
            for L in lines:
                f.write(L + "\n")

def run_diff(base:str, latest:str, out:str, invert=False, keep_order=False, wrap=False, title="", indent="\t") -> str:
    base_dict, base_order   = parse_global_file(base)
    latest_dict, latest_order = parse_global_file(latest)

    if invert:
        source_order = latest_order if keep_order else sorted(latest_dict.keys(), key=str.upper)
        missing = [k for k in source_order if k not in base_dict]
        src = latest_dict
    else:
        source_order = base_order if keep_order else sorted(base_dict.keys(), key=str.upper)
        missing = [k for k in source_order if k not in latest_dict]
        src = base_dict

    lines = emit_lines(missing, src, indent=indent)
    write_output(out, lines, wrap=wrap, title=title, indent=indent)

    base_only  = sum(1 for k in base_dict if k not in latest_dict)
    latest_only = sum(1 for k in latest_dict if k not in base_dict)
    summary = (
        f"[done] Wrote {len(missing)} lines → {out}\n"
        f"[stats] base: {len(base_dict)} keys | latest: {len(latest_dict)} keys\n"
        f"[diff] missing in latest: {base_only} | missing in base: {latest_only}"
    )
    return summary

# ---------- CLI mode (works the same as before) ----------
def cli_main():
    ap = argparse.ArgumentParser(description="Compare GTA V Global.oxt text-dumps and output missing entries.")
    ap.add_argument("PREVIOUS FILE", help="Reference file (assumed to contain the superset of keys).")
    ap.add_argument("LATEST VANILLA FILE", help="File to compare against the old file.")
    ap.add_argument("-o", "--out", default="missing_keys.txt", help="Output file.")
    ap.add_argument("--invert", action="store_true", help="Show keys present in LATEST but missing in BASE.")
    ap.add_argument("--keep-order", action="store_true", help="Preserve order from the chosen source file.")
    ap.add_argument("--wrap", action="store_true", help="Wrap output in a minimal 'Version ... { ... }' block.")
    ap.add_argument("--title", default="", help="Optional comment after Version line when using --wrap.")
    ap.add_argument("--indent", default="\\t", help="Indent to use for emitted lines (default: tab).")
    args = ap.parse_args()

    indent = args.indent.replace("\\t", "\t").replace("\\s", " ")
    summary = run_diff(args.base, args.latest, args.out,
                       invert=args.invert, keep_order=args.keep_order,
                       wrap=args.wrap, title=args.title, indent=indent)
    print(summary)

# ---------- Double-click GUI mode (no arguments) ----------
def gui_main():
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox, simpledialog
    except Exception:
        print("GUI mode requires Tkinter. Re-run from a terminal with arguments.")
        input("Press Enter to exit...")
        return

    root = tk.Tk()
    root.withdraw()

    filetypes = [("All files","*.*")]
    base = filedialog.askopenfilename(title="Select PREVIOUS FILE for Global dump", filetypes=filetypes)
    if not base:
        return
    latest = filedialog.askopenfilename(title="Select LATEST VANILLA FILE for Global dump", initialdir=os.path.dirname(base), filetypes=filetypes)
    if not latest:
        return
    out = filedialog.asksaveasfilename(title="Save output as...", defaultextension=".txt",
                                       initialdir=os.path.dirname(latest), initialfile="missing_in_latest.txt",
                                       filetypes=[("Text files","*.txt")])
    if not out:
        return

    invert = messagebox.askyesno("Direction", "Invert?\nYes = show keys that are in LATEST but missing in BASE.\nNo = show keys that are in BASE but missing in LATEST.")
    keep_order = messagebox.askyesno("Order", "Preserve source file order?")
    wrap = messagebox.askyesno("Wrap output", "Wrap in 'Version 2 30 { ... }' block?")
    title = ""
    if wrap:
        title = simpledialog.askstring("Block title (optional)", "Comment after Version line:", initialvalue="Patch Block") or ""

    summary = run_diff(base, latest, out, invert=invert, keep_order=keep_order, wrap=wrap, title=title, indent="\t")
    try:
        messagebox.showinfo("gxt_global_diff", summary)
    finally:
        # Keep console-less .pyw runs user-friendly
        pass

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        gui_main()   # double-click: show file pickers
    else:
        cli_main()   # command line: same switches as before
