import customtkinter as ctk
from customtkinter import filedialog
from tkinter import messagebox

class TextEditor:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.geometry('800x600')
        self.window.resizable(True, True)
        self.window.title('Text Editor 1.0')

        self.window.minsize(275, 275)

        self.current_file = None

        nav_frame = ctk.CTkFrame(self.window, height=25, width=800)
        nav_frame.pack(fill='x')

        save_btn = ctk.CTkButton(nav_frame, text='Save', fg_color=('grey', 'green'), command=self.save_file)
        save_btn.pack(side='right')

        load_btn = ctk.CTkButton(nav_frame, text='Load', fg_color=('grey', 'green'), command=self.load_file)
        load_btn.pack(side='right')

        text_frame = ctk.CTkFrame(self.window)
        text_frame.pack(fill='both', expand=True)

        self.text = ctk.CTkTextbox(text_frame, width=800, height=575)
        self.text.pack(fill='both', expand=True)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.bind("<Configure>", self.on_window_configure)

    def on_window_configure(self, event):
        new_width = event.width
        new_height = event.height - 25
        self.text.configure(height=new_height, width=new_width)

    def save_file(self):
        if self.current_file:
            with open(self.current_file, 'w') as f:
                f.write(self.text.get('1.0', 'end-1c'))
            messagebox.showinfo('Success!', 'File saved successfully')
        else:
            self.save_as_file()

    def save_as_file(self):
        filename = filedialog.asksaveasfilename()
        with open(filename, 'w') as f:
            f.write(self.text.get('1.0', 'end-1c'))
        self.current_file = filename
        messagebox.showinfo('Success!', 'File saved successfully')

    def load_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            with open(filename, 'r') as f:
                content = f.read()
                self.text.delete('1.0', 'end')
                self.text.insert('1.0', content)
            self.current_file = filename

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window.destroy()

if __name__ == "__main__":
    editor = TextEditor()
    editor.window.mainloop()

