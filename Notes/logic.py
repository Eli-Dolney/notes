import os

class NoteManager:
    def __init__(self, base_dir="notes"):
        self.base_dir = base_dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def create_category(self, category_name):
        category_path = os.path.join(self.base_dir, category_name)
        if not os.path.exists(category_path):
            os.makedirs(category_path)

    def delete_category(self, category_name):
        category_path = os.path.join(self.base_dir, category_name)
        if os.path.exists(category_path):
            for root, dirs, files in os.walk(category_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(category_path)

    def add_note_to_category(self, category, note_title, note_content):
        category_path = os.path.join(self.base_dir, category)
        note_path = os.path.join(category_path, f"{note_title}.txt")
        with open(note_path, "w") as note_file:
            note_file.write(note_content)

    def delete_note_from_category(self, category, note_index):
        category_path = os.path.join(self.base_dir, category)
        notes = sorted(os.listdir(category_path))
        if note_index < len(notes):
            note_path = os.path.join(category_path, notes[note_index])
            os.remove(note_path)

    def get_note_titles(self, category):
        category_path = os.path.join(self.base_dir, category)
        notes = sorted(os.listdir(category_path))
        return [os.path.splitext(note)[0] for note in notes]

    def get_note_content(self, category, note_index):
        category_path = os.path.join(self.base_dir, category)
        notes = sorted(os.listdir(category_path))
        if note_index < len(notes):
            note_path = os.path.join(category_path, notes[note_index])
            with open(note_path, "r") as note_file:
                return os.path.splitext(notes[note_index])[0], note_file.read()
        return "", ""

    def save_note_content(self, category, note_index, note_title, note_content):
        category_path = os.path.join(self.base_dir, category)
        notes = sorted(os.listdir(category_path))
        if note_index < len(notes):
            old_note_path = os.path.join(category_path, notes[note_index])
            new_note_path = os.path.join(category_path, f"{note_title}.txt")
            os.rename(old_note_path, new_note_path)
            with open(new_note_path, "w") as note_file:
                note_file.write(note_content)

    def get_categories(self):
        return [name for name in os.listdir(self.base_dir) if os.path.isdir(os.path.join(self.base_dir, name))]
