import os
import ast
import re


def unindent(lines):
    """
    Remove common indentation from string.
    """
    try:
        indent = min(len(line) - len(line.lstrip()) for line in lines if line)
    except ValueError:
        return lines
    else:
        return [line[indent:] for line in lines]


def code_block(lines, language=''):
    """
    Mark the code segment for syntax highlighting.
    """
    return ['```' + language] + unindent(lines) + ['```']


def doctest2md(lines):
    """
    Convert the given doctest to a syntax highlighted markdown segment.
    """
    is_only_code = True
    lines = unindent(lines)
    for line in lines:
        if not line.startswith('>>> ') and not line.startswith('... ') and line not in ['>>>', '...']:
            is_only_code = False
            break
    if is_only_code:
        orig = lines
        lines = []
        for line in orig:
            lines.append(line[4:])
    return lines


def doc_code_block(lines, language):
    if language == 'python':
        lines = doctest2md(lines)
    return code_block(lines, language)


def extract_docstring_from_node(source, node):
    """
    Extract the docstring from the given AST node using regular expressions.

    Args:
        source (str): The source code.
        node (AST): The AST node.

    Returns:
        str: The extracted docstring.
    """
    if hasattr(node, 'body') and isinstance(node.body, list) and len(node.body) > 0:
        first_node = node.body[0]
        if isinstance(first_node, ast.Expr) and isinstance(first_node.value, ast.Constant) and isinstance(
                first_node.value.value, str):
            docstring = first_node.value.value
            return docstring
    return None


def extract_docstrings_from_file(filepath):
    """
    Extract module, class, and function/method docstrings from a Python file.

    Args:
        filepath (str): Path to the Python file.

    Returns:
        tuple: Module docstring and a list of tuples containing kind, name, and docstring.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        source = file.read()

    tree = ast.parse(source)
    module_docstring = ast.get_docstring(tree)
    docstrings = []

    # Helper function to set parent attribute
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            class_docstring = extract_docstring_from_node(source, node)
            docstrings.append(('class', class_name, class_docstring))
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    method_name = child.name
                    method_docstring = extract_docstring_from_node(source, child)
                    docstrings.append(('method', f"{class_name}.{method_name}", method_docstring))
        elif isinstance(node, ast.FunctionDef):
            # Check if the function is inside a class by looking at its parents
            is_method = False
            parent = node
            while parent:
                if isinstance(parent, ast.ClassDef):
                    is_method = True
                    break
                parent = parent.parent if hasattr(parent, 'parent') else None
            if not is_method:
                function_name = node.name
                function_docstring = extract_docstring_from_node(source, node)
                docstrings.append(('function', function_name, function_docstring))

    return module_docstring, docstrings


def generate_markdown(module_docstring, docstrings, title):
    """
    Generate Markdown content from extracted docstrings.

    Args:
        module_docstring (str): The module docstring.
        docstrings (list): List of tuples containing kind, name, and docstring.
        title (str): The title for the Markdown content.

    Returns:
        str: Generated Markdown content.
    """
    md = []

    if module_docstring:
        md.append(f'# {title}')
        md.append('')
        md.append(module_docstring)
        md.append('')

    current_class = None
    for kind, name, docstring in docstrings:
        if kind == 'class':
            current_class = name
            md.append(f'### {kind.capitalize()} {name}')
        elif kind == 'method' and current_class and name.startswith(f"{current_class}."):
            method_name = name.split(".")[1]
            md.append(f'#### {kind.capitalize()} {method_name}')
        else:
            md.append(f'### {kind.capitalize()} {name}')
            current_class = None
        md.append('')
        if docstring:
            md.append('<details><summary>Docstring</summary>')
            md.append('')
            md.append(docstring)
            md.append('')
            md.append('</details>')
            md.append('')

    return '\n'.join(md)


def find_python_files(directory):
    """
    Recursively find all Python files in the given directory.

    Args:
        directory (str): The root directory to search for Python files.

    Returns:
        list: List of paths to Python files.
    """
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and file != os.path.basename(__file__):
                python_files.append(os.path.join(root, file))
    return python_files


def create_table_of_contents(entries):
    """
    Create a table of contents for the Markdown document.

    Args:
        entries (list): List of tuples containing the module name and docstrings.

    Returns:
        str: Table of contents in Markdown format.
    """
    toc = ["# Table of Contents", ""]
    for entry in entries:
        title, docstrings = entry
        toc.append(f"- [{title}](#{title.replace('.', '').replace(' ', '-').lower()})")
        current_class = None
        for kind, name, _ in docstrings:
            if kind == 'class':
                toc.append(f"  - [{kind.capitalize()} {name}](#{kind}-{name.replace('_', '-').lower()})")
                current_class = name
            elif kind == 'method':
                if current_class and name.startswith(f"{current_class}."):
                    toc.append(f"    - [Method {name.split('.')[1]}](#method-{name.replace('_', '-').lower()})")
                else:
                    toc.append(f"  - [{kind.capitalize()} {name}](#{kind}-{name.replace('_', '-').lower()})")
                    current_class = None
            elif kind == 'function':
                toc.append(f"  - [{kind.capitalize()} {name}](#{kind}-{name.replace('_', '-').lower()})")
    return '\n'.join(toc)


def main():
    """
    Main function to generate the README.md file from Python docstrings.
    """
    # Directory to search for Python files
    root_dir = os.getcwd()
    python_files = find_python_files(root_dir)

    readme_content = []
    toc_entries = []

    for filepath in python_files:
        module_name = os.path.splitext(os.path.relpath(filepath, root_dir))[0].replace(os.path.sep, '.')
        module_docstring, docstrings = extract_docstrings_from_file(filepath)
        toc_entries.append((module_name, docstrings))
        markdown = generate_markdown(module_docstring, docstrings, module_name)
        readme_content.append(markdown)

    toc = create_table_of_contents(toc_entries)
    with open('../README.md', 'w', encoding='utf-8') as f:
        f.write(f"# Project Documentation\n\n{toc}\n\n" + '\n\n'.join(readme_content))


if __name__ == "__main__":
    main()
