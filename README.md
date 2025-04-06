# Scene Tree Parser

This script converts an indented, human-readable scene tree with node types and properties into a .tscn scene file usable by Godot Engine.

It reads a text-based hierarchy and generates nested node definitions and property assignments based on indentation and special line prefixes.

---

## 🧾 Example Input

\\\
QuestCard (Panel)
└── HBoxContainer (HBoxContainer)
    ├── IconLabel (Label)
    │   ├── IconShadow (Control)
    │   └── IconBorder (Control)
    └── Info (VBoxContainer)
        ├── NameLabel (Label)
        │   └── NameBadge (TextureRect)
        ├── Description (Label)
        └── MetaLabel (Label)

:NameLabel.text="This is a quest"
:Description.text="Complete this for glory!"
:MetaLabel.text="📚 Daily | ⚔️ Medium"
:IconShadow.visible=true
:NameBadge.texture="res://assets/badge.png"
\\\

---

## 📦 Usage

1. Create a .txt file with your scene tree formatted as shown.
2. Place it in the same directory as scene_tree_parser.py.
3. Run the script using Python.
4. It will generate a .tscn file based on the structure and properties.

