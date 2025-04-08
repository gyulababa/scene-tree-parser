import os
import re
import argparse
import logging
from dataclasses import dataclass
from typing import Optional, Tuple, List, Dict

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Regex Caching: Compile common regex patterns once.
CLEAN_REGEX = re.compile(r"^[\s│├└─]*")
COMMENT_REGEX = re.compile(r"\s*#.*")
UID_REGEX = re.compile(r'uid="([^"]+)"')

@dataclass
class Node:
    name: str
    type: str
    parent: Optional[str] = None
    full_path: Optional[str] = None

def clean_line(line: str) -> str:
    """
    Remove leading box-drawing characters and extra spaces using a cached regex.
    """
    return CLEAN_REGEX.sub("", line).strip()

def get_indent_level(line: str) -> int:
    """
    Compute the indentation level based on leading spaces or box-drawing characters.
    """
    match = CLEAN_REGEX.match(line)
    if match:
        prefix = match.group(0)
        return len(prefix) // 4
    return 0

def extract_uid_from_existing_tscn(tscn_path: str) -> Optional[str]:
    """
    Extract uid from an existing .tscn file, if available.
    """
    if os.path.exists(tscn_path):
        try:
            with open(tscn_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
            match = UID_REGEX.search(first_line)
            if match:
                uid = match.group(1)
                logger.info(f"Found existing UID: {uid}")
                return uid
        except Exception as e:
            logger.error(f"Error reading {tscn_path}: {e}")
    logger.warning("No UID found.")
    return None

def validate_line_format(line: str, line_num: int) -> bool:
    """
    Validate that a given line meets expected formatting rules.
    """
    if "(" not in line:
        logger.error(f"Line {line_num} does not have a valid format: '{line}'")
        return False
    return True

def parse_scene_tree(lines: List[str], verbose: bool = False) -> Tuple[List[Node], Dict[str, Dict[str, str]]]:
    """
    Parse the text-based node tree into a list of Node objects and a dictionary of properties.
    Uses a list (path_stack) to track the current node hierarchy.
    """
    nodes: List[Node] = []
    properties: Dict[str, Dict[str, str]] = {}
    path_stack: List[str] = []

    for line_num, line in enumerate(lines, start=1):
        original_line = line.rstrip("\n")

        # Skip empty lines
        if not original_line.strip():
            if verbose:
                logger.debug(f"Skipped line {line_num}: empty")
            continue

        # Process property definitions (lines starting with ":")
        if original_line.strip().startswith(":"):
            try:
                prop_def = original_line.strip()[1:]
                node_prop, value = prop_def.split("=", 1)
                node_name, prop_key = node_prop.split(".", 1)
                value = value.strip().strip('"')
                node_name = node_name.strip()
                prop_key = prop_key.strip()
                if node_name not in properties:
                    properties[node_name] = {}
                properties[node_name][prop_key] = value
                if verbose:
                    logger.debug(f"Parsed property for node '{node_name}': {prop_key} = '{value}'")
            except Exception as e:
                logger.error(f"Error parsing property on line {line_num}: '{original_line}': {e}")
            continue

        # Remove in-line comments using cached regex
        line_no_comment = COMMENT_REGEX.sub("", original_line)
        clean_text = clean_line(line_no_comment)

        if not clean_text:
            if verbose:
                logger.debug(f"Skipped line {line_num}: no content after cleaning.")
            continue

        indent_level = get_indent_level(original_line)
        if verbose:
            logger.debug(f"Line {line_num}: indent level {indent_level}, text: '{clean_text}'")
        if not validate_line_format(clean_text, line_num):
            continue

        try:
            # Use string slicing and splitting to extract node name and type.
            name_part, type_part = clean_text.split("(", 1)
            name = name_part.strip()
            node_type = type_part.rstrip(") ").strip()
        except Exception as e:
            logger.error(f"Error parsing node on line {line_num}: '{clean_text}': {e}")
            continue

        # Adjust the path stack based on the current indent level
        while len(path_stack) > indent_level:
            path_stack.pop()
        path_stack.append(name)
        full_path = "/".join(path_stack)
        parent_path = None
        if len(path_stack) > 1:
            parent_path = "/".join(path_stack[:-1])

        if verbose:
            logger.debug(f"Node parsed: {name} ({node_type}), Parent: {parent_path}, Full Path: {full_path}")
        node = Node(name=name, type=node_type, parent=parent_path, full_path=full_path)
        nodes.append(node)

    return nodes, properties

def write_tscn(nodes: List[Node], properties: Dict[str, Dict[str, str]], out_path: str, uid: Optional[str] = None, verbose: bool = False):
    """
    Generate the .tscn content from Node objects and properties, then write the result to the output path.
    """
    uid_attr = f' uid="{uid}"' if uid else ""
    lines = [f'[gd_scene format=3{uid_attr}]']
    for node in nodes:
        if node.parent is None:
            lines.append(f'[node name="{node.name}" type="{node.type}"]')
        else:
            lines.append(f'[node name="{node.name}" type="{node.type}" parent="{node.parent}"]')

        node_props = properties.get(node.name, {})
        for key, value in node_props.items():
            lines.append(f'{key} = "{value}"')
        lines.append("")  # Blank line for readability

    if verbose:
        logger.info("\nGenerated .tscn Preview:\n" + "\n".join(lines))

    try:
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        logger.info(f"Scene file saved as: {out_path}")
    except Exception as e:
        logger.error(f"Error writing file {out_path}: {e}")

def parse_arguments():
    """
    Parse command-line arguments for configuration.
    """
    parser = argparse.ArgumentParser(description="Parse a node tree and generate a .tscn file for Godot.")
    parser.add_argument("--tree-file", type=str, default="tree.txt",
                        help="Path to the text file with the node tree.")
    parser.add_argument("--output-dir", type=str, default=os.getcwd(),
                        help="Directory where the generated .tscn file will be saved.")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose/debug output.")
    return parser.parse_args()

def main():
    args = parse_arguments()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    try:
        with open(args.tree_file, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
        logger.info(f"Successfully read file: {args.tree_file}")
    except Exception as e:
        logger.error(f"Failed to read file {args.tree_file}: {e}")
        return

    nodes, properties = parse_scene_tree(lines, verbose=args.verbose)

    if not nodes:
        logger.error("No valid nodes were parsed. Please check the input file for proper formatting.")
        return

    # Use the name of the first node as the output scene file name.
    output_filename = f"{nodes[0].name}.tscn"
    output_path = os.path.join(args.output_dir, output_filename)
    uid = extract_uid_from_existing_tscn(output_path)
    write_tscn(nodes, properties, output_path, uid=uid, verbose=args.verbose)

if __name__ == "__main__":
    main()
