import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from logic import NoteManager
from mind_map import MindMap

class NoteTakingApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Note Taking System")
        self.root.geometry("800x600")
        self.note_manager = NoteManager()
        self.mind_map = MindMap()

        self.setup_ui()

    def setup_ui(self):
        self.main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Category Management
        self.category_frame = ttk.LabelFrame(self.main_frame, text="Categories", padding="10 10 10 10")
        self.category_frame.grid(row=0, column=0, sticky=(tk.N, tk.S), padx=10, pady=10)

        self.add_category_button = ttk.Button(self.category_frame, text="Add Category", command=self.add_category)
        self.add_category_button.grid(row=0, column=0, sticky=tk.EW, pady=5)

        self.delete_category_button = ttk.Button(self.category_frame, text="Delete Category", command=self.delete_category)
        self.delete_category_button.grid(row=1, column=0, sticky=tk.EW, pady=5)

        self.category_listbox = tk.Listbox(self.category_frame, height=15)
        self.category_listbox.grid(row=2, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), pady=5)
        self.category_listbox.bind('<<ListboxSelect>>', self.load_notes)
        self.category_frame.columnconfigure(0, weight=1)
        self.category_frame.rowconfigure(2, weight=1)

        # Note Management
        self.note_frame = ttk.LabelFrame(self.main_frame, text="Notes", padding="10 10 10 10")
        self.note_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W), padx=10, pady=10)

        self.add_note_button = ttk.Button(self.note_frame, text="Add Note", command=self.add_note)
        self.add_note_button.grid(row=0, column=0, sticky=tk.EW, pady=5)

        self.delete_note_button = ttk.Button(self.note_frame, text="Delete Note", command=self.delete_note)
        self.delete_note_button.grid(row=0, column=1, sticky=tk.EW, pady=5)

        self.note_listbox = tk.Listbox(self.note_frame, height=10)
        self.note_listbox.grid(row=1, column=0, columnspan=2, sticky=(tk.N, tk.S, tk.E, tk.W), pady=5)
        self.note_listbox.bind('<<ListboxSelect>>', self.load_note_content)
        self.note_frame.columnconfigure(0, weight=1)
        self.note_frame.columnconfigure(1, weight=1)
        self.note_frame.rowconfigure(1, weight=1)

        ttk.Label(self.note_frame, text="Title:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.note_title_entry = ttk.Entry(self.note_frame)
        self.note_title_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(self.note_frame, text="Content:").grid(row=3, column=0, sticky=tk.NW, pady=5)
        self.note_text = tk.Text(self.note_frame, wrap=tk.WORD, height=10)
        self.note_text.grid(row=3, column=1, sticky=(tk.N, tk.S, tk.E, tk.W), pady=5)
        self.note_frame.rowconfigure(3, weight=1)

        self.save_note_button = ttk.Button(self.note_frame, text="Save Note", command=self.save_note)
        self.save_note_button.grid(row=4, column=0, columnspan=2, sticky=tk.EW, pady=5)

        # Mind Map
        self.mind_map_button = ttk.Button(self.main_frame, text="Generate Mind Map", command=self.generate_mind_map)
        self.mind_map_button.grid(row=1, column=1, sticky=tk.E, padx=10, pady=10)

        self.update_category_list()

    def add_category(self):
        category_name = simpledialog.askstring("Category Name", "Enter category name:")
        if category_name:
            self.note_manager.create_category(category_name)
            self.update_category_list()

    def delete_category(self):
        current_category = self.category_listbox.get(tk.ACTIVE)
        if current_category:
            self.note_manager.delete_category(current_category)
            self.update_category_list()

    def add_note(self):
        note_title = simpledialog.askstring("Note Title", "Enter note title:")
        current_category = self.category_listbox.get(tk.ACTIVE)
        if current_category and note_title:
            self.note_manager.add_note_to_category(current_category, note_title, "")
            self.load_notes()

    def delete_note(self):
        current_category = self.category_listbox.get(tk.ACTIVE)
        selected_note = self.note_listbox.curselection()
        if current_category and selected_note:
            note_index = selected_note[0]
            self.note_manager.delete_note_from_category(current_category, note_index)
            self.load_notes()

    def load_notes(self, event=None):
        current_category = self.category_listbox.get(tk.ACTIVE)
        if current_category:
            notes = self.note_manager.get_note_titles(current_category)
            self.note_listbox.delete(0, tk.END)
            for note in notes:
                self.note_listbox.insert(tk.END, note)
            self.note_text.delete("1.0", tk.END)
            self.note_title_entry.delete(0, tk.END)

    def load_note_content(self, event=None):
        current_category = self.category_listbox.get(tk.ACTIVE)
        selected_note = self.note_listbox.curselection()
        if current_category and selected_note:
            note_index = selected_note[0]
            note_title, note_content = self.note_manager.get_note_content(current_category, note_index)
            print(f"Loading note: {note_title}, Content: {note_content}")  # Debug print
            self.note_title_entry.delete(0, tk.END)
            self.note_title_entry.insert(0, note_title)
            self.note_text.delete("1.0", tk.END)
            self.note_text.insert(tk.END, note_content)

    def save_note(self):
        current_category = self.category_listbox.get(tk.ACTIVE)
        selected_note = self.note_listbox.curselection()
        if current_category and selected_note:
            note_index = selected_note[0]
            note_title = self.note_title_entry.get()
            note_content = self.note_text.get("1.0", tk.END).strip()
            print(f"Saving note: {note_title}, Content: {note_content}")  # Debug print
            self.note_manager.save_note_content(current_category, note_index, note_title, note_content)
            self.load_notes()

    def update_category_list(self):
        categories = self.note_manager.get_categories()
        self.category_listbox.delete(0, tk.END)
        for category in categories:
            self.category_listbox.insert(tk.END, category)

    def generate_mind_map(self):
        current_category = self.category_listbox.get(tk.ACTIVE)
        if current_category:
            try:
                self.mind_map.generate(self.note_manager, current_category)
                messagebox.showinfo("Mind Map", f"Mind map for '{current_category}' generated successfully.")
            except Exception as e:
                messagebox.showerror("Mind Map Error", str(e))
        else:
            try:
                self.mind_map.generate(self.note_manager)
                messagebox.showinfo("Mind Map", "Mind map for all categories generated successfully.")
            except Exception as e:
                messagebox.showerror("Mind Map Error", str(e))

    def run(self):
        self.root.mainloop()
