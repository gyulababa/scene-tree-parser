# 🌳 Scene Tree Parser for Godot

This Python tool allows you to write Godot scene hierarchies using a clean, readable, indented text format—and automatically converts them into `.tscn` files usable by the Godot Engine.

---

## ✨ Features

- **Human-Readable Scene Parsing:**  
  Write your scene trees in a plain-text file using intuitive indented hierarchy and Godot node notation.

- **Inline Property Assignment:**  
  Assign properties directly inline using a simple syntax.

- **TS Scene File Generation:**  
  Produces ready-to-use `.tscn` files while preserving existing scene UIDs if present.

- **Enhanced Parsing Efficiency:**  
  Uses regex caching and efficient string slicing to optimize the parsing process.

- **Robust Error Handling & Logging:**  
  Improved validations and granular logging (via Python's `logging` module) to help debug format errors and parsing issues.

- **Structured Data Model:**  
  Adopts a modern data model using Python's `dataclasses` for clear definition and maintainability of Node objects.

- **Command-Line Interface (CLI):**  
  Accepts CLI arguments for specifying input/output paths and toggling verbose debugging output.

---

## 🧾 Input Format

Write your scene hierarchy in a `.txt` file using this style:

### 📄 Example Input

<pre>
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
</pre>

---

## 📦 Usage

### 1. Create Your Scene Tree

- Save the above structure in a file (e.g., `tree.txt`).
- Place it in the same directory as `scene_tree_parser.py` (or specify a different file via CLI).

### 2. Run the Parser

```bash
python scene_tree_parser.py --tree-file tree.txt --output-dir <output_directory> --verbose
```

### 3. Output

- The script generates a file like `QuestCard.tscn`.
- If a `.tscn` with the same name already exists, its UID is preserved.

---

## 🔠 Property Assignment Syntax

Inline properties use the following format:

```
:NodeName.property_name=value
```

**Examples:**
```
:TitleLabel.text="Hello World"
:HealthBar.value=100
:Sprite.texture="res://icon.png"
```

---

## 📐 Node Tree Writing Guide

To keep scene definitions readable and consistent, follow these conventions:

### ✅ Do's

- Use `└──` for the last child in a group.
- Use `├──` for intermediate children.
- Indent with 4 spaces per level.
- Always include node type: `NodeName (NodeType)`
- Start with the root node and maintain proper nesting.

**Example:**

<pre>
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
</pre>

---

### 🚫 Don’ts

- ❌ Don’t mix tabs and spaces — use **only** 4 spaces.
- ❌ Don’t omit node types.
- ❌ Don’t use placeholder comments like `... (more nodes here)`.
- ❌ Don’t leave misaligned `│` pipes.

---

## 🔧 How It Works

### Parsing

- **Indentation Detection:**  
  Uses tree-drawing symbols (`├──`, `└──`, `│`) and regex-based cleaning to determine indentation levels.
  
- **Efficient String Operations:**  
  Uses efficient string slicing to extract node names and types.

- **Regex Caching:**  
  Common regular expressions are compiled once at module load for performance.

- **Structured Data Model:**  
  Node information is stored in a `Node` dataclass, ensuring clear, maintainable structure.

- **Error Handling & Logging:**  
  Implements enhanced validation of input lines and logs errors/warnings using Python’s `logging` module.

### Generation

- Produces a valid `.tscn` file conforming to Godot 3 standards.
- Optionally preserves UID from an existing `.tscn` file.
- Supports CLI arguments for flexible file input/output management.

---

## 📁 Output Example

For the input shown earlier, this will produce a `.tscn` file similar to:

```tscn
[gd_scene format=3 uid="abc123"]

[node name="QuestCard" type="Panel"]
[node name="HBoxContainer" type="HBoxContainer" parent="QuestCard"]
[node name="IconLabel" type="Label" parent="QuestCard/HBoxContainer"]
[node name="IconShadow" type="Control" parent="QuestCard/HBoxContainer/IconLabel"]
[node name="IconBorder" type="Control" parent="QuestCard/HBoxContainer/IconLabel"]
[node name="Info" type="VBoxContainer" parent="QuestCard/HBoxContainer"]
[node name="NameLabel" type="Label" parent="QuestCard/HBoxContainer/Info"]
[node name="NameBadge" type="TextureRect" parent="QuestCard/HBoxContainer/Info/NameLabel"]
[node name="Description" type="Label" parent="QuestCard/HBoxContainer/Info"]
[node name="MetaLabel" type="Label" parent="QuestCard/HBoxContainer/Info"]

text = "This is a quest"
text = "Complete this for glory!"
text = "📚 Daily | ⚔️ Medium"
visible = "true"
texture = "res://assets/badge.png"
```

---

## 🧪 Debug Output

When running in verbose mode, the script prints helpful logs during parsing—for example:

```
DEBUG: Line 5: indent level 2, text: 'NameLabel (Label)'
DEBUG: Node parsed: NameLabel (Label), Parent: Info, Full Path: QuestCard/HBoxContainer/Info/NameLabel
```

---

## 🚀 Recent Enhancements

These updates have improved the parser significantly:
- **Regex Caching:** Compiled all frequently used regex patterns at module load time for performance gains.
- **String Slicing:** Leveraged efficient string slicing to extract node details quickly and reliably.
- **Enhanced Error Handling:**  
  Adopted Python's `logging` module for detailed error, warning, and debug output.
- **Data Model Improvements:**  
  Introduced a `Node` dataclass to clearly encapsulate each node's data (name, type, parent, full_path) for better maintainability and future scalability.

---

## 📃 License

MIT — free to use and modify.

---

## 🙌 Contributions

Suggestions, improvements, and PRs welcome!