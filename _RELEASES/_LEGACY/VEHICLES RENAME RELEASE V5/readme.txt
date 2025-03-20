RenameV
Created by ShifuGuru 20/03/2025


gta5-mods.com:
https://www.gta5-mods.com/misc/replaced-game-names

Beta testing available here:
https://github.com/shifuguru/renamev

[For easier viewing of this file use Word Wrap from your text editors View settings]

[Info]
English support only

Updated for patch 3411 - Dec '24
I have also released a version for Enhanced which I have verified as working,
check my tutorial on my github page.
https://github.com/shifuguru/

This mod will likely require updating every patch,
I have recently created a python script which should make this easier to update in future,
I may release the script to those interested

=ε/̵͇̿̿/’̿’̿ ̿  (˵ ͡° ͜ʖ ͡°˵)  ===>

Ensure you keep a backup of your ~vehicles.meta~ file,
especially if you have made your own edits.
Feel free to edit the values yourself.
RDE support as of RDE 4.1,
if it doesn't work just use the manual method to change the vehicle make names of several vehicles.

The provided ~vehicles.meta~ file also adds brands that don't exist in Vanilla GTA.
This requires my A_Global dlcpack to provide the additional Vehicle Brands.
 The game will very likely crash if you do not add the included dlcpack.

The vehicles.meta files in the dlc_patch folder swap a lot of the online dlc cars and aren't necessarily required to install, but important for perfectionists, otherwise you'll get Honda Supra instead of Toyota Supra for Karin Jester Classic (jester3).

IMPORTANT: Backup your vehicles.meta file, in case you have previously edited it for modded vehicles, dashboards, wheel sizes etc.



[Installation]

0. Use OpenIV or Codewalker and enable Edit Mode:

Navigate to the following folders and drag/drop to add/replace files from their respective folders:

1. ..\mods\update\update.rpf\common\data\levels\gta5\
- Replace VEHICLES.META
- Alternatively use the Manual Changes file

[Important: Must be done in OpenIV]
2. ..\mods\update\update2.rpf\x64\data\lang\american_rel.rpf\
- Replace GLOBAL.GXT with global.oxt


3. ..\mods\update\x64\dlcpacks\
- Copy A_GLOBAL folder (dlc.rpf should be inside)


4. ..\mods\update\update.rpf\common\data\
a. Right-click > Edit: DLCLIST.XML
b. Add to end of list before </Paths>:

	<Item>dlcpacks:/A_Global/</Item>

c. Save


5. Launch the game!


Comment any bugs or issues
https://www.gta5-mods.com/misc/replaced-game-names
