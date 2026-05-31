from jinja2 import Environment, FileSystemLoader
import os

OUTPUT_DIR = "dist"

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("index.html")
index_html = template.render()

with open(os.path.join(OUTPUT_DIR, "index.html"), 'w', encoding='utf-8') as f:
        f.write(index_html)
