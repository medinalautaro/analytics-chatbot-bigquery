import os

# folders we do NOT want in the tree
IGNORE_DIRS = {
    ".venv",
    "venv",
    "__pycache__",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    "node_modules",
    "site-packages",
    ".idea",
    ".vscode",
    "dist",
    "build"
}

def tree(directory, prefix=""):
    entries = sorted(os.listdir(directory))
    entries = [e for e in entries if e not in IGNORE_DIRS]

    for index, name in enumerate(entries):
        path = os.path.join(directory, name)
        connector = "└── " if index == len(entries) - 1 else "├── "

        print(prefix + connector + name)

        if os.path.isdir(path):
            extension = "    " if index == len(entries) - 1 else "│   "
            tree(path, prefix + extension)

print(os.path.basename(os.getcwd()) + "/")
tree(".")