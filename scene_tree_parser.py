import os
import re

def clean_line(line):
    # Remove tree symbols but preserve node format
    return re.sub(r"^[\s│├└─]*", "", line).strip()

def get_indent_level(line):
    # Determine indent level by dividing the prefix length by 4.
    match = re.match(r"^([\s│├└─]*)", line)
    if not match:
        return 0
    prefix = match.group(1)
    return len(prefix) // 4

def parse_scene_tree(lines):
    nodes = []
    properties = {}
    path_stack = {}

    for line_num, line in enumerate(lines, start=1):
        original_line = line.rstrip("\n")

        if not original_line.strip():
            print(f"⚠️ Skipped line {line_num}: '{original_line}' (empty)")
            continue

        # Handle property lines (those starting with a colon)
        if original_line.strip().startswith(":"):
            try:
                prop_def = original_line.strip()[1:]
                node_prop, value = prop_def.split("=", 1)
                node_name, prop_key = node_prop.split(".", 1)
                value = value.strip().strip('"')
                if node_name not in properties:
                    properties[node_name] = {}
                properties[node_name][prop_key.strip()] = value
                print(f"🔧 Property -> Node: {node_name.strip()}, {prop_key.strip()} = \"{value}\"")
            except Exception as e:
                print(f"⚠️ Failed to parse property at line {line_num}: '{original_line.strip()}' → {e}")
            continue

        # Clean the line and compute the indent level using the helper function
        clean_line_text = re.sub(r"[│├└─]+", "", original_line).strip()
        prefix = original_line[:original_line.index(clean_line_text)]
        indent_level = len(prefix) // 4  # Correctly compute level: 4 characters per indent

        print(f"\n🔹 Line {line_num}: '{original_line}'")
        print(f"  ✂️ Cleaned Line: '{clean_line_text}'")
        print(f"  🔢 Indentation Level: {indent_level}")

        if "(" not in clean_line_text:
            print(f"⚠️ Skipped line {line_num}: '{original_line}' (unrecognized format)")
            continue

        # Split the cleaned line into node name and type
        name, node_type = clean_line_text.split("(", 1)
        name = name.strip()
        node_type = node_type.strip(") ")

        if indent_level == 0:
            parent_path = None  # Root node
            full_path = name
        elif indent_level == 1:
            parent_path = "."  # Direct child of root
            full_path = name
        else:
            # For deeper levels, use the parent's full_path to create the full path
            parent_node = path_stack[indent_level - 1]
            parent_path = parent_node["name"] if indent_level == 2 else parent_node["full_path"]
            full_path = f"{parent_path}/{name}"

        # Save current node in the path stack for future children
        path_stack[indent_level] = {"name": name, "full_path": full_path}

        print(f"  📦 Node: {name} ({node_type})")
        print(f"  📁 Parent Path: {parent_path if parent_path is not None else '[root]'}")
        print(f"  📄 Full Path: {full_path}")

        nodes.append({
            "name": name,
            "type": node_type,
            "parent": parent_path,
            "full_path": full_path
        })

    return nodes, properties

def write_tscn(tree, properties, out_path):
    lines = ['[gd_scene load_steps={} format=3]'.format(len(tree))]
    for node in tree:
        # If the node's parent is None, output "None"; otherwise, output its value.
        parent_val = node["parent"] if node["parent"] is not None else "None"
        lines.append(f'[node name="{node["name"]}" type="{node["type"]}" parent="{parent_val}"]')
        props = properties.get(node["name"], {})
        for key, value in props.items():
            lines.append(f'{key} = "{value}"')
        lines.append("")  # spacer line

    print("\n📝 .tscn Preview:\n")
    print("\n".join(lines))
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"\n✅ Saved scene file as: {out_path}")

def main():
    root = os.getcwd()
    path = os.path.join(root, "tree.txt")

    print(f"📂 Working directory: {root}")
    print(f"📄 Reading: {path}\n")

    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    print("📜 Raw tree.txt content:")
    for l in lines:
        print(" ", l)
    print("\n🔍 Parsing Debug Info:\n")

    tree, properties = parse_scene_tree(lines)

    print("\n🧩 Parsed Scene Tree:")
    for node in tree:
        print(f' - {node["name"]} ({node["type"]}) — Parent: {node["parent"]}')
    if tree:
        root_name = tree[0]["name"]
        tscn_path = os.path.join(root, f"{root_name}.tscn")
        write_tscn(tree, properties, tscn_path)
    else:
        print("❌ No valid nodes found.")

if __name__ == "__main__":
    main()
