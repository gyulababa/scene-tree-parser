# 🌳 Scene Tree Parser for Godot

This Python tool allows you to write Godot scene hierarchies using a clean, readable, indented text format — and automatically converts them into `.tscn` files usable by Godot Engine.

---

## ✨ Features

- Parse human-readable scene trees with node types.
- Assign properties inline using simple syntax.
- Outputs a ready-to-use `.tscn` file with optional UID preservation.
- Debug-friendly output during parsing and file generation.

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

- Save the above structure in a file named `tree.txt`.
- Place it in the same directory as `scene_tree_parser.py`.

### 2. Run the Parser

```bash
python scene_tree_parser.py
```

### 3. Output

- The script generates a file like `QuestCard.tscn`.
- If a `.tscn` with the same name already exists, its UID will be preserved.

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

- Detects indentation level using tree-drawing symbols (`├──`, `└──`, `│`).
- Extracts node name and type from lines like `NodeName (NodeType)`.
- Tracks hierarchy with a stack.
- Supports optional inline properties using `:Node.property=value`.

### Generation

- Produces a valid `.tscn` file using Godot 3 format.
- Optionally preserves UID from a preexisting `.tscn`.

---

## 📁 Output Example

For the input shown earlier, this will produce a `.tscn` like:

```tscn
[gd_scene format=3 uid="abc123"]

[node name="QuestCard" type="Panel"]
[node name="HBoxContainer" type="HBoxContainer" parent="QuestCard"]
[node name="IconLabel" type="Label" parent="HBoxContainer"]
[node name="IconShadow" type="Control" parent="IconLabel"]
[node name="IconBorder" type="Control" parent="IconLabel"]
[node name="Info" type="VBoxContainer" parent="HBoxContainer"]
[node name="NameLabel" type="Label" parent="Info"]
[node name="NameBadge" type="TextureRect" parent="NameLabel"]
[node name="Description" type="Label" parent="Info"]
[node name="MetaLabel" type="Label" parent="Info"]

text = "This is a quest"
text = "Complete this for glory!"
text = "📚 Daily | ⚔️ Medium"
visible = "true"
texture = "res://assets/badge.png"
```

---

## 🧪 Debug Output

The script prints helpful logs during parsing:

```
🔹 Line 5: '    ├── NameLabel (Label)'
  ✂️ Cleaned Line: 'NameLabel (Label)'
  🔢 Indentation Level: 2
  📦 Node: NameLabel (Label)
  📁 Parent Path: Info
  📄 Full Path: Info/NameLabel
```

---

## 🚀 Future Ideas

- Support for `export` hints or groups.
- Godot 4 support with scene format upgrades.
- CLI arguments for input/output paths.
- Optional reusable templates/snippets.

---

## 📃 License

MIT — free to use and modify.

---

## 🙌 Contributions

Suggestions, improvements, and PRs welcome!
