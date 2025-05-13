import os
import subprocess
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_app():
    try:
        import tkinter
        from PIL import Image, ImageTk
        import requests
    except ImportError as e:
        print(f"Error: {e}")
        print("Please install required packages first:")
        print("pip install tk pillow requests")
        return
    
    print("Running the Course Catalog App...")
    subprocess.run([sys.executable, "course-app.py"])

def create_exe():
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    print("Creating executable...")
    # PyInstaller command to create a single executable
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name=CourseCatalog',
        '--add-data=courses.json;.',
        'course-app.py'
    ]
    
    subprocess.run(cmd)
    print("\nExecutable created in the 'dist' folder!")

def main_menu():
    clear_screen()
    print("""
    *****************************
    * COURSE CATALOG APP MANAGER *
    *****************************
    
    1. Run the Course Catalog App
    2. Create Executable (PyInstaller)
    3. Exit
    """)
    
    while True:
        choice = input("Enter your choice (1-3): ")
        if choice == '1':
            run_app()
            break
        elif choice == '2':
            create_exe()
            input("\nPress Enter to return to main menu...")
            main_menu()
            break
        elif choice == '3':
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()