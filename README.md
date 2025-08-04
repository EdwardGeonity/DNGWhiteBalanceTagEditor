[IMAGE 2025-08-04 23:45:30](https://github.com/user-attachments/assets/40a297ed-3152-4905-b69f-8b66bb93e5f6)
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

