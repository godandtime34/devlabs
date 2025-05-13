# YouTube Course Catalog App

A simple Tkinter application that organizes YouTube playlists into a visual catalog with cards.

## Features

- Display YouTube playlists as cards with thumbnails
- Add new playlists with URL, title, and thumbnail
- Open playlists directly in your browser
- Responsive grid layout with scrollable interface
- Option to bundle as standalone executable

## Requirements

- Python 3.6+
- Tkinter (usually included with Python)
- Pillow (`pip install pillow`)
- Requests (`pip install requests`)
- PyInstaller (optional, for creating executable)

## Installation

1. Clone the repository or download the files
2. Install dependencies:

```bash
pip install pillow requests pyinstaller
```

## Usage

Run the main menu:

```bash
python main.py
```

Choose an option:

1. Run the application
2. Create executable (requires PyInstaller)

## File Structure

```bash
course-app/
├── main.py            # Main menu/launcher
├── course-app.py      # Main application
├── courses.json       # Stores playlist data
└── README.md          # This file
```

## Creating Executable

From the main menu (option 2) or manually:

```bash
pyinstaller --onefile --windowed --name=CourseCatalog --add-data=courses.json;. course-app.py
```

The executable will be created in the `dist` folder. Update the course.json file in the `dist` folder to show more courses on the app.


<img width="1280" alt="Screenshot 2025-05-13 at 4 46 15 PM" src="https://github.com/user-attachments/assets/bcd0b85a-a936-40c8-95c8-f2b58e2b03a3" />
