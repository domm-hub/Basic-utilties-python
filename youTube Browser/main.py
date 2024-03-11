import tkinter as tk
from customtkinter import *
from pytube import Search, YouTube
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

class FastTitle(CTkLabel):
    def __init__(self, master, font_size=10, **kwargs):
        font = CTkFont("Calibri", font_size)
        super().__init__(master, font=font, **kwargs)

def display_image_from_url(url, label):
    def load_image():
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            image.thumbnail((160 * 2, 90 * 2))  # Resize thumbnail
            photo = ImageTk.PhotoImage(image)
            label.configure(image=photo)
            label.image = photo  # Keep a reference to the image to prevent garbage collection
        except Exception as e:
            print(f"Error loading image from URL: {e}")

    # Create a thread to load the image asynchronously
    thread = threading.Thread(target=load_image)
    thread.daemon = True  # Daemonize the thread to prevent it from blocking program exit
    thread.start()

def open_video(Y: YouTube, path: str):
    
    try:
        stream = Y.streams.get_highest_resolution()
        if not stream:
            raise Exception("No suitable video stream found.")
        
        if path:
            stream.download(output_path=path)
            import tqdm
            for i in tqdm.gui.tqdm(stream.filesize_approx):
                pass
            import os
            os.startfile(path)
    except:
        pass
    if Y.age_restricted:
        from tkinter import messagebox
        
        messagebox.showerror("Age restriction", f"{Y.title} is age restricted, please access it from youtube.")

def searchvid(term, cont, num_results=9): 
     # Default to 9 results
    clear_frame(cont)
    results = Search(term).results[:num_results]  # Fetch only the specified number of results
    for i, video in enumerate(results):
        video: YouTube = video
        
        def do(video):
            from customtkinter import filedialog
            from tkinter import messagebox
            if video.length // 60 > 15:
                if messagebox.askyesno("Download", "File is larger than 15 min. Do you want to download?"):
                    path = filedialog.askdirectory()
                    if path:
                        video_thread = threading.Thread(target=open_video, args=(video, path))
                        video_thread.start()

                        # Wait for the video thread to finish
                        video_thread.join()
            else:
                path = filedialog.askdirectory()
                if path:
                    video_thread = threading.Thread(target=open_video, args=(video, path))
                    video_thread.start()
        
        row = i // 1
        col = i % 1
        data_frame = CTkFrame(cont, bg_color=("black", "white"))
        data_frame.pack(fill="x", padx=10, pady=10,)
        
        imagelabel = CTkLabel(data_frame, text=f"{video.length // 60} minutes", cursor="hand2", wraplength=150)
        display_image_from_url(video.thumbnail_url, imagelabel)
        imagelabel.pack(side="left")
        import datetime
        
        title = FastTitle(data_frame, font_size=50, text=video.title, wraplength=500)
        title.pack()
        description = FastTitle(data_frame, font_size=20, text=f"   {video.views} views, Author: {video.author}, Posted {video.publish_date.strftime('%d/%m/%Y')}, Length {video.length} seconds or {video.length // 60} minutes")
        description.pack()

        imagelabel.bind("<Button-1>", lambda event, v=video: do(v))

window = CTk()
window.title("Youtube Browser")
window.geometry("550x400")
window.minsize(1000, 900)

Search_Frame = CTkFrame(window)
Search_Frame.pack(fill="x", padx=10, pady=10)

ytimg = Image.open("Youtube.jpg")
ytimg.thumbnail((100, 100))
ytimg = ImageTk.PhotoImage(ytimg)

yt_icon = CTkLabel(Search_Frame, width=100, image=ytimg, text="")
yt_icon.pack(side="right")

search = CTkEntry(Search_Frame)
search.pack(side="left", fill="x", expand=True)
search.insert(tk.END, "Popular Videos")

results_var = tk.StringVar()
results_var.set("9")  # Default to 9 results
results_entry = CTkEntry(Search_Frame, textvariable=results_var, width=100)
results_entry.pack(side="left")

Search_Button = CTkButton(Search_Frame, text="Search!", width=10, command=lambda: threading.Thread(target=searchvid, args=(search.get(), youtube_container, int(results_var.get()))).start())
Search_Button.pack(side="left")

youtube_container = CTkScrollableFrame(window)
youtube_container.pack(fill="both", expand=True, padx=10, pady=10)

window.mainloop()
