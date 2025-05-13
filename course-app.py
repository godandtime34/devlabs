import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import webbrowser
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading

class CourseCatalogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Course Catalog")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize variables
        self.courses = []
        self.load_courses()
        
        # Create UI
        self.create_widgets()
        
    def load_courses(self):
        try:
            with open('courses.json', 'r') as f:
                self.courses = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.courses = []
    
    def save_courses(self):
        with open('courses.json', 'w') as f:
            json.dump(self.courses, f, indent=4)
    
    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        header_frame.pack(fill='x', padx=10, pady=10)
        
        title_label = tk.Label(header_frame, text="Course Catalog", font=('Arial', 20, 'bold'), 
                              fg='white', bg='#2c3e50')
        title_label.pack(side='left', padx=20)
        
        add_btn = tk.Button(header_frame, text="+ Add Playlist", font=('Arial', 10), 
                           command=self.add_playlist_dialog, bg='#3498db', fg='white')
        add_btn.pack(side='right', padx=20)
        
        # Main content area
        self.canvas = tk.Canvas(self.root, bg='#f0f0f0')
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='#f0f0f0')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Display courses
        self.display_courses()
    
    def display_courses(self):
        # Clear existing courses
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        if not self.courses:
            empty_label = tk.Label(self.scrollable_frame, text="No courses added yet. Click '+ Add Playlist' to add one.", 
                                 font=('Arial', 12), bg='#f0f0f0')
            empty_label.pack(pady=50)
            return
        
        # Display courses in a grid
        rows = (len(self.courses) + 2) // 3  # 3 columns
        for i in range(rows):
            row_frame = tk.Frame(self.scrollable_frame, bg='#f0f0f0')
            row_frame.pack(fill='x', padx=10, pady=10)
            
            for j in range(3):
                idx = i * 3 + j
                if idx >= len(self.courses):
                    break
                
                course = self.courses[idx]
                self.create_course_card(row_frame, course)
    
    def create_course_card(self, parent, course):
        card_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, borderwidth=1)
        card_frame.pack(side='left', padx=10, pady=10, fill='both', expand=True)
        
        # Course image
        img_frame = tk.Frame(card_frame, bg='white', height=150, width=250)
        img_frame.pack(pady=(10, 5))
        img_frame.pack_propagate(False)
        
        try:
            response = requests.get(course['thumbnail'])
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((250, 150), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            img_label = tk.Label(img_frame, image=photo)
            img_label.image = photo  # Keep a reference
            img_label.pack(fill='both', expand=True)
        except:
            # Fallback if image can't be loaded
            img_label = tk.Label(img_frame, text="No Image", bg='white')
            img_label.pack(fill='both', expand=True)
        
        # Course title
        title_label = tk.Label(card_frame, text=course['title'], font=('Arial', 12, 'bold'), 
                             bg='white', wraplength=230)
        title_label.pack(pady=(0, 10))
        
        # View button
        view_btn = tk.Button(card_frame, text="View Playlist", font=('Arial', 10), 
                           command=lambda url=course['url']: webbrowser.open(url),
                           bg='#3498db', fg='white')
        view_btn.pack(pady=(0, 10))
        
        # Delete button
        delete_btn = tk.Button(card_frame, text="Delete", font=('Arial', 8), 
                             command=lambda c=course: self.delete_course(c),
                             bg='#e74c3c', fg='white')
        delete_btn.pack(pady=(0, 10))
    
    def add_playlist_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Playlist")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        
        tk.Label(dialog, text="YouTube Playlist URL:", font=('Arial', 12)).pack(pady=(20, 5))
        url_entry = tk.Entry(dialog, width=40, font=('Arial', 12))
        url_entry.pack(pady=5)
        
        tk.Label(dialog, text="Playlist Title:", font=('Arial', 12)).pack(pady=(10, 5))
        title_entry = tk.Entry(dialog, width=40, font=('Arial', 12))
        title_entry.pack(pady=5)
        
        tk.Label(dialog, text="Thumbnail URL (optional):", font=('Arial', 12)).pack(pady=(10, 5))
        thumbnail_entry = tk.Entry(dialog, width=40, font=('Arial', 12))
        thumbnail_entry.pack(pady=5)
        
        def add_course():
            url = url_entry.get().strip()
            title = title_entry.get().strip()
            thumbnail = thumbnail_entry.get().strip()
            
            if not url or not title:
                messagebox.showerror("Error", "URL and Title are required!")
                return
            
            # Basic URL validation
            if "youtube.com/playlist" not in url and "youtu.be" not in url:
                messagebox.showerror("Error", "Please enter a valid YouTube playlist URL")
                return
            
            # Default thumbnail if not provided
            if not thumbnail:
                # This is a placeholder - you might want to extract the actual thumbnail from YouTube
                thumbnail = "https://img.youtube.com/vi/default/maxresdefault.jpg"
            
            self.courses.append({
                'title': title,
                'url': url,
                'thumbnail': thumbnail
            })
            
            self.save_courses()
            self.display_courses()
            dialog.destroy()
        
        add_btn = tk.Button(dialog, text="Add Playlist", command=add_course, 
                           bg='#2ecc71', fg='white', font=('Arial', 12))
        add_btn.pack(pady=20)
    
    def delete_course(self, course):
        if messagebox.askyesno("Confirm", f"Delete '{course['title']}'?"):
            self.courses.remove(course)
            self.save_courses()
            self.display_courses()

def main():
    root = tk.Tk()
    app = CourseCatalogApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()