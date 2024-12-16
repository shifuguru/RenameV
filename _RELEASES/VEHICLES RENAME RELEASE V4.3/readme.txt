Created by ShifuGuru 7/01/2024 
- Happy New Year! 

Authentic Vehicle Names Overhaul


[Info]
English support only at this stage!

Updated for patch 3095

This mod will need updating every patch which is really annoying, but the way I've created the mod, should mean that only a couple files will need updating per patch. 

Ensure you keep a backup of Vehicles.meta, the file changes some vehicle brands to ones that don't exist in Vanilla GTA and required my A_Global dlcpack to provide the Vehicle Brands. 

The changes are much more accurate than other mods I've tested, and hopefully should be easier to manage each time there is a game update compared to my previous version of this mod from 2022. 


[Installation]

0. Use OpenIV and enable Edit Mode (F6):

Navigate to the following folders and drag/drop to add/replace files from their respective folders: 

1. ..\mods\update\update.rpf\common\data\levels\gta5\ 
- Replace VEHICLES.META 


2. ..\mods\update\update2.rpf\x64\data\lang\american_rel.rpf\ 
- Replace GLOBAL.GXT


3. ..\mods\update\x64\dlcpacks\ 
- Copy A_GLOBAL folder (dlc.rpf should be inside)
- Copy A_GLOBAL2 folder (dlc.rpf should be inside)


4. ..\mods\update\update.rpf\common\data\ 
a. Right-click > Edit: DLCLIST.XML 
b. Add to end of list before </Paths>:  
<Item>dlcpacks:/A_Global/</Item>
<Item>dlcpacks:/A_Global2/</Item>
c. Save 


5. ..\mods\update\update.rpf\dlc_patch\..

Install all vehicles.meta files in each respective dlc_patch folder,
..\common\data\levels\gta5\.. 


6. Launch the game!



IMPORTANT: Backup your vehicles.meta file, in case you have previously edited it for modded vehicles, dashboards, wheel sizes etc. 


Comment any bugs or issues


