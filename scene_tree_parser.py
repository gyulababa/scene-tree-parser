import os
import re

def clean_line(line):
    return re.sub(r"^[\s│├└─]*", "", line).strip()

def get_indent_level(line):
    match = re.match(r"^([\s│├└─]*)", line)
    if not match:
        return 0
    prefix = match.group(1)
    return len(prefix) // 4

def extract_uid_from_existing_tscn(tscn_path):
    if os.path.exists(tscn_path):
        with open(tscn_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            match = re.search(r'uid="([^"]+)"', first_line)
            if match:
                uid = match.group(1)
                print(f"🔑 Found existing UID: {uid}")
                return uid
    print("⚠️ No UID found.")
    return None

def parse_scene_tree(lines):
    nodes = []
    properties = {}
    path_stack = {}

    for line_num, line in enumerate(lines, start=1):
        original_line = line.rstrip("\n")

        if not original_line.strip():
            print(f"⚠️ Skipped line {line_num}: '{original_line}' (empty)")
            continue

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

        clean_line_text = re.sub(r"[│├└─]+", "", original_line).strip()
        prefix = original_line[:original_line.index(clean_line_text)]
        indent_level = len(prefix) // 4

        print(f"\n🔹 Line {line_num}: '{original_line}'")
        print(f"  ✂️ Cleaned Line: '{clean_line_text}'")
        print(f"  🔢 Indentation Level: {indent_level}")

        if "(" not in clean_line_text:
            print(f"⚠️ Skipped line {line_num}: '{original_line}' (unrecognized format)")
            continue

        name, node_type = clean_line_text.split("(", 1)
        name = name.strip()
        node_type = node_type.strip(") ")

        if indent_level == 0:
            parent_path = None
            full_path = name
        elif indent_level == 1:
            parent_path = "."
            full_path = name
        else:
            parent_node = path_stack[indent_level - 1]
            parent_path = parent_node["name"] if indent_level == 2 else parent_node["full_path"]
            full_path = f"{parent_path}/{name}"

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

def write_tscn(tree, properties, out_path, uid=None):
    uid_attr = f' uid="{uid}"' if uid else ""
    lines = [f'[gd_scene format=3{uid_attr}]']
    for node in tree:
        name = node["name"]
        type_ = node["type"]
        parent = node["parent"]

        if parent is None:
            lines.append(f'[node name="{name}" type="{type_}"]')
        else:
            lines.append(f'[node name="{name}" type="{type_}" parent="{parent}"]')

        props = properties.get(name, {})
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
    tree_path = os.path.join(root, "tree.txt")

    print(f"📂 Working directory: {root}")
    print(f"📄 Reading: {tree_path}\n")

    with open(tree_path, 'r', encoding='utf-8') as f:
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
        uid = extract_uid_from_existing_tscn(tscn_path)
        write_tscn(tree, properties, tscn_path, uid=uid)
    else:
        print("❌ No valid nodes found.")

if __name__ == "__main__":
    main()
