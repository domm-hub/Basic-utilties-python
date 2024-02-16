import qrcode
from PIL import ImageTk
from customtkinter import filedialog as f
import customtkinter as ctk

window = ctk.CTk()
window.title("QRCode Generator")
window.geometry("600x600")
window.minsize(600, 600)

def createqr():
    data = URL_TextBox.get() 
    qr = qrcode.make(data)
    qr_image = ImageTk.PhotoImage(qr)
    Photo.configure(image=qr_image)
    Photo.image = qr_image

bigfont = ctk.CTkFont("Calibri", 30)

label = ctk.CTkLabel(window, text="QRCode Generator", font=bigfont)
label.pack()

label = ctk.CTkLabel(window, text="URL or Data:")
label.pack(pady=10)

URL_TextBox = ctk.CTkEntry(window)
URL_TextBox.pack()

Photo = ctk.CTkLabel(window, text="")
Photo.pack(pady=10)

create_btn = ctk.CTkButton(window, text="Create!", command=createqr)
create_btn.pack(pady=40)

# "Save" button
save_btn = ctk.CTkButton(window, text="Save", command=lambda: save_qr())
save_btn.pack()

def save_qr():
    if hasattr(Photo, "image") and Photo.image:
        filename = f.asksaveasfilename(title="Save Image As", defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if filename:
            qr = qrcode.make(URL_TextBox.get())
            qr.save(filename)
    else:
        from tkinter import messagebox
        messagebox.showinfo("Info", "Please Make A QR Code")

window.mainloop()
