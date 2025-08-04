<img width="400" height="295" alt="image" src="https://github.com/user-attachments/assets/a2bfdbc8-39fa-49b4-b297-1cf03f857442" />



# DNG White Balance Tag Editor

A simple GUI tool for editing the AsShotNeutral white balance values in DNG raw image files.



## Features

- View current white balance values from DNG files
- Edit RGB multipliers for white balance!

- Save modified copies of DNG files
- Preserves all original image data while only modifying the white balance tag

## Installation

1. Clone this repository
2. Install required packages:

pip install -r requirements.txt
text


## Usage

1. Run the program: `python DNGWhiteBalanceTagEditor.py`
2. Click "Open DNG" to load a DNG file
3. Edit the R, G, B values as needed
4. Click "Save Copy" to save a modified version

## Notes

- Always work on copies of your original DNG files
- The program may not work with all DNG variants as the format can vary
- Some raw processors may ignore or override these values

## Version

Current version: 0.3

