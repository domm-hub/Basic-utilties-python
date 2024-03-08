import tkinter as tk
from customtkinter import *
from pytube import Search
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading

def display_image_from_url(url, label):
    def load_image():
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            image.thumbnail((160, 90))  # Resize thumbnail
            photo = ImageTk.PhotoImage(image)
            label.configure(image=photo)
            label.image = photo  # Keep a reference to the image to prevent garbage collection
        except Exception as e:
            print(f"Error loading image from URL: {e}")

    # Create a thread to load the image asynchronously
    thread = threading.Thread(target=load_image)
    thread.daemon = True  # Daemonize the thread to prevent it from blocking program exit
    thread.start()

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def open_video(video_id):
    import webbrowser
    webbrowser.open_new_tab(f"https://www.youtube.com/watch?v={video_id}")

def searchvid(term, cont, num_results=9):  # Default to 9 results
    clear_frame(cont)
    results = Search(term).results[:num_results]  # Fetch only the specified number of results
    for i, video in enumerate(results):
        row = i // 3
        col = i % 3
        label = CTkLabel(cont, text=f"ID: {video.video_id}\nTitle: {video.title}", wraplength=150)
        label.bind("<Button-1>", lambda event, video_id=video.video_id: open_video(video_id))


        display_image_from_url(video.thumbnail_url, label)
        label.grid(row=row, column=col, padx=5, pady=5)

window = CTk()
window.title("Youtube Browser")
window.geometry("550x400")
window.minsize(550, 400)

Search_Frame = CTkFrame(window)
Search_Frame.pack(fill="x", padx=10, pady=10)

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
