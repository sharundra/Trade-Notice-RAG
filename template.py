import os
from pathlib import Path

source_folder_name = "src"

list_of_files = [

    f"{source_folder_name}/__init__.py",
    f"{source_folder_name}/config.py",
    f"{source_folder_name}/ingest.py",
    f"{source_folder_name}/vector_store.py",
    f"{source_folder_name}/rag_chain.py",
    "app.py",
    "requirements.txt",
    "README.md"
]


for filepath in list_of_files:
    fp = filepath
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if fp.endswith("/"):
        os.makedirs(filepath, exist_ok=True)
        continue
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
    else:
        print(f"file is already present at: {filepath}")