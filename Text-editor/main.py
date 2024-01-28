import sys
import customtkinter as ctk
from customtkinter import filedialog
from tkinter import messagebox
import CTkMenuBar
import chlorophyll
import pygments.lexers
import webbrowser
import darkdetect

class FastTitle(ctk.CTkLabel):
    def __init__(self, master, font_size=20, **kwargs):
        font = ctk.CTkFont("Calibri", font_size)
        super().__init__(**kwargs, font=font, master=master)

class CustomText(chlorophyll.CodeView):
    def __init__(self, indent_after_colon=True, **kwargs):
        color = "white" if darkdetect.isLight() else "black"
        super().__init__(**kwargs)
        self.bind("<KeyRelease>", self.do)
        self.leading_whitespace = 0

    def do(self, event):
        if event.keysym == ":" or event.keysym.lower() == "colon":
            self.insert(chars="\n\t", index=ctk.END)

class TextEditor:
    def __init__(self):
        self.current_file = ""
        
        self.window = ctk.CTk()
        self.window.geometry('800x600')
        self.window.resizable(True, True)
        self.window.title('Text editor 2.0.2 ')
        self.window.minsize(275, 275)

        def on_key(event):
            if event.keysym == 'Control_L' and not ctrl_pressed[0]:
                ctrl_pressed[0] = True
            elif event.keysym == 's' and ctrl_pressed[0]:
                print("Ctrl + S pressed")
                self.save_file()
            elif event.keysym == 'l' and ctrl_pressed[0]:
                print("Ctrl + L pressed")
                self.load_file()
            elif event.keysym == 'h' and ctrl_pressed[0]:
                print("Ctrl + H pressed")
                self.show_find_replace_popup()
            elif event.keysym == 'equal' or (event.keysym == 'plus' and ctrl_pressed[0]):
                print("Ctrl + Plus pressed")
                self.increase_font_size()
            elif event.keysym == 'minus' and ctrl_pressed[0]:
                print("Ctrl + minus pressed")
                self.decrease_font_size()

        def on_key_release(event):
            if event.keysym == 'Control_L':
                ctrl_pressed[0] = False

        ctrl_pressed = [False]

        self.window.bind('<Key>', on_key)
        self.window.bind('<KeyRelease>', on_key_release)

        self.menu = CTkMenuBar.CTkMenuBar(self.window, bg_color=["white", "black"])
        self.cascade = self.menu.add_cascade(text="File")
        self.dropdown1 = CTkMenuBar.CustomDropdownMenu(self.cascade)
        self.dropdown1.add_option(option="Save", command=self.save_file)
        self.dropdown1.add_option(option="Load", command=self.load_file)
        self.dropdown1.add_option(option="Find and replace", command=self.show_find_replace_popup)
        self.lang = ctk.CTkComboBox(self.dropdown1, values=("Python", "Plain Text"), command=self.changelang)
        self.lang.pack(pady=10)

        self.cascade2 = self.menu.add_cascade(text="Other")
        self.dropdown2 = CTkMenuBar.CustomDropdownMenu(self.cascade2)
        self.dropdown2.add_option(option="Go to my GitHub Webpage", command=lambda: webbrowser.open_new_tab("www.github.com/domm-hub"))
        self.dropdown2.add_option("Exit", command=lambda: sys.exit(0))
        self.dropdown2.add_option("Settings", command=self.settings)

        text_frame = ctk.CTkFrame(self.window)
        text_frame.pack(fill='both', expand=True)

        self.font_size = 15  # Default font size
        self.font = ctk.CTkFont("Calibri", self.font_size)
        
        self.textt = CustomText(master=text_frame, width=800, height=575, indent_after_colon=True, font=self.font)  # Ensure indentation
        self.textt.pack(fill='both', expand=True)

        self.commandlineinput()
        try:
            if sys.argv[1].endswith(".py"):
                self.textt.configure(lexer=pygments.lexers.Python3Lexer)
                print("This is a python file.")
            else:
                print("Switching to text based...")
        except:
            print("No ARGS provided")
        

        self.find_replace_popup = ctk.CTkToplevel(self.window)
        self.find_replace_popup.withdraw()
        self.find_replace_popup.geometry("350x175")
        self.find_replace_popup.resizable(False, False)
        self.find_replace_popup.title("Find and Replace")

        find_label = ctk.CTkLabel(self.find_replace_popup, text="Find:")
        find_label.pack()

        self.find_entry_replace = ctk.CTkEntry(self.find_replace_popup)
        self.find_entry_replace.pack()

        replace_label = ctk.CTkLabel(self.find_replace_popup, text="Replace:")
        replace_label.pack(pady=5)

        self.replace_entry = ctk.CTkEntry(self.find_replace_popup)
        self.replace_entry.pack(pady=5)

        find_button = ctk.CTkButton(self.find_replace_popup, text="Replace", command=self.find_replace)
        find_button.pack()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.bind("<Configure>", self.on_window_configure)

    def on_window_configure(self, event):
        new_width = event.width
        new_height = event.height - 25
        self.textt.configure(height=new_height, width=new_width)

    def commandlineinput(self):
        if len(sys.argv) > 1:
            # Assume the first argument (after the script name) is the filename
            filename = sys.argv[1]
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                    self.textt.delete('1.0', 'end')
                    self.textt.insert('1.0', content)
                    self.current_file = filename
            except FileNotFoundError:
                print(f"Error: File not found: {filename}")
            except Exception as e:
                print(str(e))


    def changelang(self, *args, **kwargs):
        if self.lang.get() == "Python":
            self.textt.configure(lexer=pygments.lexers.Python3Lexer)
        else:
            self.textt.configure(lexer=pygments.lexers.TextLexer)

    def save_file(self, do=None):
        if self.current_file:
            with open(self.current_file, 'w') as f:
                f.write(self.textt.get('1.0', 'end-1c'))
            messagebox.showinfo('Success!', 'File saved successfully')
        else:
            self.save_as_file()

    def save_as_file(self):
        filename = filedialog.asksaveasfilename()
        if filename:
            with open(filename, 'w') as f:
                f.write(self.textt.get('1.0', 'end-1c'))
            self.current_file = filename
            messagebox.showinfo('Success!', 'File saved successfully')



    def settings(self):
        settings_window = ctk.CTkToplevel()
        settings_window.title("Settings")

        frame = ctk.CTkScrollableFrame(settings_window)
        frame.pack()

        title = FastTitle(frame, text="Font Size:")
        title.pack(side="top")

        combo = ctk.CTkComboBox(frame, values=['8', '9', '10', '11', '12', '13', '14', '16', '18', '20', '22', '24', '26', '28', '30', '32', '34', '36', '40', '48', '56', '64', '72'])
        combo.pack()

        title = FastTitle(frame, text="Appearance mode:")
        title.pack(pady=10)

        combo2 = ctk.CTkComboBox(frame, values=["Light", "Dark", f"System default ({darkdetect.theme()})"])
        combo2.pack()

        def setvars():
            try:
                if int(combo.get()) > 72:
                    messagebox.showinfo("Error", "The number: " + combo.get() + " is too big so we lowered it to 48")
                    font = ctk.CTkFont("Calibri", size=48)
                    self.textt.configure(font=font)
                    return None

                font = ctk.CTkFont("Calibri", size=int(combo.get()))
                self.textt.configure(font=font)
                try:
                    # Update appearance mode for both the main window and navigation bar
                    selected_mode = combo2.get()
                    if selected_mode == f"System default ({darkdetect.theme()})":
                        selected_mode = darkdetect.theme()
                    settings_window._set_appearance_mode(selected_mode)
                    self.window._set_appearance_mode(selected_mode)
                    self.menu._set_appearance_mode(selected_mode)
                    self.cascade._set_appearance_mode(selected_mode)
                    self.cascade2._set_appearance_mode(selected_mode)
                except Exception as e:
                    messagebox.showerror("Error: ", str(e))
                settings_window.destroy()

            except Exception as e:
                messagebox.showerror("ERROR", f"The input {combo.get()} is faulty. Error: {str(e)}")

        done_btn = ctk.CTkButton(frame, text="Done!", command=setvars)
        done_btn.pack(pady=10)

        settings_window.mainloop()

    def load_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                    self.textt.delete('1.0', 'end')
                    self.textt.insert('1.0', content)
                self.current_file = filename
            except:
                try:
                    with open(filename, 'rb') as f:
                        content = f.read()
                        self.textt.delete('1.0', 'end')
                        self.textt.insert('1.0', content)
                        self.current_file = filename
                except Exception as e:
                    messagebox.showerror("FATAL ERROR", "ERROR: " + str(e))

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window.destroy()

    def find_replace(self):
        find_text = self.find_entry_replace.get()
        replace_text = self.replace_entry.get()

        # Implement find and replace functionality
        content = self.textt.get("1.0", ctk.END)
        new_content = content.replace(find_text, replace_text.replace("\n", ""))

        # Update the text widget with the modified content
        self.textt.delete("1.0", ctk.END)
        self.textt.insert("1.0", new_content)

        # Hide the find and replace popup
        self.find_replace_popup.withdraw()

    def show_find_replace_popup(self):
        self.find_replace_popup.deiconify()

    def increase_font_size(self):
        self.font_size += 1
        if self.font_size > 72:
            self.font_size = 72
        self.font.configure(size=self.font_size)
        self.textt.configure(font=self.font)

    def decrease_font_size(self):
        self.font_size -= 1
        if self.font_size < 8:
            self.font_size = 8
        self.font.configure(size=self.font_size)
        self.textt.configure(font=self.font)

if __name__ == "__main__":
    editor = TextEditor()
    editor.window.mainloop() 
