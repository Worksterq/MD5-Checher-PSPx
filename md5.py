import hashlib
from hashlib import md5
import tkinter as tk
from tkinter import filedialog, ttk
import pyperclip
import os

class MD5ComparatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MD5 Checker for PSPx by Workster")
        self.root.attributes("-alpha", 0.9)
        self.root.configure(bg='#2E2E2E')
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "colex1.png")
        self.icon_image = tk.PhotoImage(file=icon_path)
        self.root.tk.call("wm", "iconphoto", self.root._w, self.icon_image)
        self.dark_mode = tk.BooleanVar()
        self.configure_styles()

        introduction_text = "Вы можете подсчитать контрольную сумму MD5 любого файла и сравнить его с другим."
        introduction_label = tk.Label(self.root, text=introduction_text, font=('Helvetica', 12, 'bold'), fg='#FFFFFF', bg='#2E2E2E')
        introduction_label.pack(pady=10)
        
        self.create_widgets()

        self.icon_label = tk.Label(self.root, image=self.icon_image, background='#2E2E2E')
        self.icon_label.pack(side=tk.RIGHT, padx=10)
        self.icon_label.bind("<Button-1>", self.open_website)

    def open_website(self, event):
        webbrowser.open("https://www.pspx.ru/forum/index.php")

    def configure_styles(self):
        style = ttk.Style()
        style.configure('TButton', padding=10, font=('Helvetica', 10))
        style.configure('TFrame', background='#2E2E2E')
        style.configure('TLabel', font=('Helvetica', 10, 'bold'), foreground='#FFFFFF', background='#2E2E2E')
        style.configure('TEntry', font=('Helvetica', 10), fieldbackground='#FFFFFF')
        style.configure('Result.TLabel', font=('Helvetica', 12, 'bold'), pady=10)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, style='TFrame')
        main_frame.pack(pady=20, padx=20)

        self.create_file_frame(main_frame, 'Файл 1:', 'file_path_entry1', 'md5_entry1')
        self.create_file_frame(main_frame, 'Файл 2:', 'file_path_entry2', 'md5_entry2')

        self.result_label = ttk.Label(self.root, text="", font=('Helvetica', 12, 'bold'), style='Result.TLabel')
        self.result_label.pack()

        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Копировать MD5", command=self.copy_md5)
        self.root.bind("<Button-3>", self.show_context_menu)

    def create_file_frame(self, parent, label_text, entry_name, md5_entry_name):
        frame = ttk.Frame(parent, style='TFrame')
        frame.pack(pady=10, fill='both', expand=True)

        label = ttk.Label(frame, text=label_text, style='TLabel')
        label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        entry = ttk.Entry(frame, width=45, font=('Helvetica', 10), style='TEntry')
        entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        browse_button = ttk.Button(frame, text="Обзор", command=lambda e=entry, m=md5_entry_name: self.browse_file(e, m),
                                   style='TButton')
        browse_button.grid(row=0, column=2, padx=5, pady=5, sticky='w')

        md5_label = ttk.Label(frame, text="MD5:", font=('Helvetica', 10, 'bold'), style='TLabel')
        md5_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        md5_entry = ttk.Entry(frame, width=32, font=('Helvetica', 10), style='TEntry')
        md5_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        setattr(self, entry_name, entry)
        setattr(self, md5_entry_name, md5_entry)
        md5_entry.bind("<Button-3>", lambda event, entry=md5_entry: self.show_context_menu(event, entry))

    def browse_file(self, entry, md5_entry_name):
        file_path = filedialog.askopenfilename()
        entry.delete(0, tk.END)
        entry.insert(0, file_path)
        self.update_md5_entry(getattr(self, md5_entry_name), file_path)

    @staticmethod
    def calculate_md5(file_path):
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def update_md5_entry(self, entry, file_path):
        md5_value = self.calculate_md5(file_path)
        entry.delete(0, tk.END)
        entry.insert(0, md5_value)

        md5_entry1 = self.md5_entry1.get()
        md5_entry2 = self.md5_entry2.get()

        if md5_entry1 and md5_entry2:
            text = "Файлы одинаковые" if md5_entry1 == md5_entry2 else "Файлы разные!"
            self.result_label.config(text=text, style='Result.TLabel',
                                     foreground='green' if text == "Файлы одинаковые" else 'red')

    def copy_md5(self):
        md5_entry = self.root.focus_get()
        if isinstance(md5_entry, tk.Entry):
            md5_value = md5_entry.get()
            pyperclip.copy(md5_value)
            self.result_label.config(text="Скопировано!", style='Result.TLabel', foreground='blue')

    def show_context_menu(self, event, entry=None):
        if entry is None:
            entry = self.root.winfo_containing(event.x_root, event.y_root)
        if isinstance(entry, tk.Entry):
            self.context_menu.post(event.x_root, event.y_root)

if __name__ == "__main__":
    root = tk.Tk()
    app = MD5ComparatorApp(root)
    root.mainloop()
