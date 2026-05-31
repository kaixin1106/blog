from jinja2 import Environment, FileSystemLoader
from pathlib import Path

root_path = Path.cwd()
OUTPUT_DIR = root_path/"dist"

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("index.html")
index_html = template.render()

if not OUTPUT_DIR.exists():
    OUTPUT_DIR.mkdir()

with open(OUTPUT_DIR/"index.html", 'w', encoding='utf-8') as f:
    f.write(index_html)
