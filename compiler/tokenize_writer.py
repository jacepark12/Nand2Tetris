from typing import List

from compiler.compile_engine import Tree, TreeElement

SPACE = "  "


def format_value(value: str) -> str:
    if value == "<":
        return "&lt;"
    elif value == ">":
        return "&gt;"
    elif value == '"':
        return "&quot;"
    elif value == "&":
        return "&amp;"
    else:
        return value


class TokenizeWriter:

    def __init__(self, *, compiled_tree) -> None:
        self.compiled_tree: Tree = compiled_tree
        self.xml_lines: List[str] = []
        self.tag_stack: List[str] = []
        self.indent_level: int = 1

    def write_to_xml(self, output_path: str) -> None:
        root = self.compiled_tree.root

        self.tag_stack.append(root.value)
        self.xml_lines.append(f"<{root.value}>")

        for child in root.children:
            self.explore_child(child)
        self.xml_lines.append(f"</{root.value}>")

        with open(output_path, "w") as f:
            for line in self.xml_lines:
                f.write(f"{line}\n")

    def explore_child(self, tree_element: TreeElement) -> None:

        if tree_element.is_leaf:
            tag = self.tag_stack.pop()

            tag_value = f"{format_value(tree_element.value)}"
            self.xml_lines.append(
                f"{SPACE * self.indent_level}<{tag}> {tag_value} </{tag}>"
            )
            return
        else:
            self.tag_stack.append(tree_element.value)

        has_child_leaf: bool = (
            len([x for x in tree_element.children if x.is_leaf is True]) > 0
        )
        if has_child_leaf is False:
            self.xml_lines.append(f"{SPACE * self.indent_level}<{tree_element.value}>")
            self.indent_level += 1
        for child in tree_element.children:
            self.explore_child(child)
        if has_child_leaf is False:
            self.indent_level -= 1
            self.xml_lines.append(f"{SPACE * self.indent_level}</{tree_element.value}>")

        return
