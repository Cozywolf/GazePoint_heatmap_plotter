# Heatmap plotter for GazePoint eye-tracker data #

This script will process the raw output from Gazepoint Analysis software, plot the heatmap for each condition per subject and overall plots per condition across subjects. The heatmap plotting functions were modified from https://github.com/TobiasRoeddiger/GazePointHeatMap by TobiasRoeddiger, which Python 3 support was added and supports additional heatmap output options. 

*What the script does*
1. Running codes block by block with Visual Studio Code (VSCode) Python Interactive Window
2. Directly read the Gazepoint Analyzer output csv files and insert the correspoding UnixTime
3. Read the eventTimestamp file to automatically parse the raw data for trials/conditions
4. Can plot heatmap with transparent background, on a shared background, or use background per condition
5. Automatically generate heatmaps for each individuals/trials and aggregate across subjects with the same condition name

*Structuring the event timestamps file, see exampleTimestamp.csv*
1. The first column should be named "events" (lowercase) and each row should contains event names
2. Event should be named as "<eventname>_<trial>_Start" and "<eventname>_<trial>_End" (case sensitive)
3. Event Start and End should always be paired
4. Start from the second column each column is for one participant. The name should be the same as the file names in line 24 in plotHeatmap.py
5. The time should be in a 10 digit UnixTime, decimals do not matter

*Preparing background images (if needed)*
1. The images should be in png format, the script will remove alpha layer automatically
2. Ideally the image dimension should be the same as defined in line 41 and 42 in plotHeatmap.py
3. If the image is smaller, it will be centered and black boarders will be added

*Preparing datafiles (gazepoint)*
1. Export data files from GazePoint Analysis
2. Rename the file to <participant>_fixations.csv, the participant name should be the same as in line 24 in plotHeatmap.py and event timestamp files

*How to use*
1. Make sure numpy and pandas packages are installed and it is recommended to use VSCode for block by block execution.
2. Run Block 1 in plotHeatmap.py to generate folders automatically
3. Carefully review comments in Block 2 and enter all required info and files to the corresponding folders before running 
4. Run Block 3 to load all the packages and functions
5. Run Block 4 to read the event timestamps from the csv file
6. Run Block 5, which will automatically generate all the heatmaps to save to designated folders