# RePKG GUI - Wallpaper Engine Wallpaper Extractor

A graphical interface tool based on Python and tkinter for batch extraction and conversion of Wallpaper Engine wallpaper files.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

## 📋 Project Introduction

RePKG GUI is a user-friendly graphical tool specifically designed for handling Wallpaper Engine's wallpaper files. It provides an intuitive interface to invoke the [RePKG](https://github.com/notscuffed/repkg) tool, supports batch extraction of PKG files and processing of wallpapers in direct file format.

### ✨ Main features

- 🖥️ **Graphical Interface** - Simple and easy-to-use GUI interface, no command line operation required
- 📦 **Batch Processing** - Support batch extraction of all wallpapers in Steam Workshop
- 🔄 **Dual Format Support** - Support both PKG file and direct file format
- 📊 **Real-time Progress** - Display processing progress and detailed logs
- 🎯 **Intelligent Recognition** - Automatically identify the wallpaper type and select the appropriate processing method
- 📝 **Project Information** - Extract the project name from project.json as the folder name
- ⚙️ **Rich Options** - Support all command line options of RePKG

## 🎯 Supported file formats

### PKG file format
- ✅ Standard Wallpaper Engine PKG format
- ✅ Automatically unpack and convert TEX files to images
- ✅ Extract all resource files

### Direct file formats
- ✅ Directories containing project.json
- ✅ Video wallpapers (.mp4, .webm, etc.)
- ✅ Static image wallpapers
- ✅ Web wallpapers and other formats

## 🚀 Quick Start

### Prerequisites

- Windows 10/11
- Python 3.7+ (if running from source)
- [RePKG.exe](https://github.com/notscuffed/repkg/releases) tool

### Method 1: Download the executable file (recommended)

1. From [Releases](https://github. Download the latest `RePKG-GUI.exe` from the [Releases](https://github. com/jiangdengke/repkg-gui-wallpaper-extractor/releases) to download the latest `RePKG-GUI.exe`
2. Download [RePKG.exe](https://github.com/notscuffed/repkg/releases)
3. Run `RePKG-GUI.exe`

### Method 2: Run from source

# Clone the repository
git clone https://github.com/jiangdengke/repkg-gui-wallpaper-extractor. git
cd repkg-gui-wallpaper-extractor

# Run the program
python repkg_gui_batch.py
```

## 📖 Instructions

### 1. Basic Settings

1. After starting the program, first click the "Browse" button to select the location of the `RePKG.exe` file
2. The program will automatically set the default path of Steam Workshop

### 2. Single file extraction

In the "Single Extract" tab:
- Select the PKG or TEX file to extract
- Set the output directory
- Adjust the options as needed
- Click "Start Extract"

### 3. Batch extraction (recommended)

In the "Batch Extract" tab:
- Confirm the Steam Workshop directory path (usually `C:\Program Files (x86)\Steam\steamapps\workshop\content\431960`)
- Set the batch output directory
- Select processing options:
- ✅ Process PKG files
- ✅ Process direct file directories
- ✅ Use project name as folder name
- Click "Scan Directory" to view the number of projects that can be processed
- Click "Start Batch Extract"

### 4. View file information

In the "Info View" tab:
- Select a PKG file
- View the list of included files and project information

## 🖼️ Interface preview

![Main interface](img/img.png)

## 🛠️ Building the executable

If you want to build the exe yourself:

# Install dependencies
pip install pyinstaller

# Build the exe file
pyinstaller --onefile --windowed --name "RePKG-GUI" repkg_gui.py

# The generated exe file is located in the dist/ directory



## 🔧 Configuration Options

### Extraction options
- **Recursive search** (`-r`): Search subdirectories
- **TEX conversion mode** (`-t`): Specially process TEX files
- **Single directory output** (`-s`): Put all files in one directory
- **Copy project files** (`-c`): Copy project.json and preview images
- **Use project name** (`-n`): Use the project name as the folder name
- **Do not convert TEX** (`--no-tex-convert`): Keep the original format of TEX files
- **Overwrite files** (`--overwrite`): Overwrite existing files

### Filtering options
- **Ignore extension** (`-i`): Skip files with the specified extension
- **Extract only extension** (`-e`): Only extract files with the specified extension

## 🤝 Contribution

Welcome to contribute code! Please follow the steps below:

1. Fork this project Fork this project Create your feature branch (`git checkout -b feature/AmazingFeature`) Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`) Create a Pull Request

## 📝 Update Log

### v1.0.0 (2025-07-04)
- 🎉 Initial version released
- ✨ Support batch extraction of PKG files and direct file formats
- 🖥️ User-friendly GUI interface
- 📊 Real-time progress display and detailed logs
- 🔧 Rich configuration options

## 🐛 Bug Feedback

If you have any problems or suggestions, please:
1. Check the [Issues](https://github.com/jdkzwl/repkg-gui-wallpaper-extractor/issues) page
2. Create a new issue to describe the problem Provide detailed error information and screenshots

## 📄 License

This project is released under the MIT license - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

<div align="center">
<img src="./img/jetbrains.svg" alt="JetBrains" width="150"/>
<br>
<b>Special thanks to <a href="https://www. jetbrains.com/">JetBrains</a> for providing free IDE licenses for open source projects</b>
</div>

## 📞 Contact

- GitHub: [@jiangdengke](https://github.com/jiangdengke)
- Issues: [项目Issues页面](https://github.com/jiangdengke/repkg-gui-wallpaper-extractor/issues)

---

⭐ If this project is helpful to you, please give a Star to support it!
