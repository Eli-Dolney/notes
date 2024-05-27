import os
from graphviz import Digraph

class MindMap:
    def __init__(self, output_dir="mind_maps"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate(self, note_manager, category=None):
        dot = Digraph(comment='Mind Map')
        
        if category:
            self.add_category_to_dot(dot, note_manager, category)
        else:
            categories = note_manager.get_categories()
            for category in categories:
                self.add_category_to_dot(dot, note_manager, category)

        output_path = os.path.join(self.output_dir, f"mind_map_{category if category else 'all'}")
        dot.render(output_path, view=True)

    def add_category_to_dot(self, dot, note_manager, category):
        dot.node(category, category)
        notes = note_manager.get_note_titles(category)
        for i, note in enumerate(notes):
            note_label = f"{category}_note{i+1}"
            dot.node(note_label, note)
            dot.edge(category, note_label)
