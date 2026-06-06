from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import markdown
import frontmatter

root_path = Path.cwd()
OUTPUT_DIR = root_path/"dist"
POSTS_DIR = root_path/"posts"
TEMPLATES_DIR = root_path/"templates"

if not OUTPUT_DIR.exists():
    OUTPUT_DIR.mkdir()

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
env.filters["markdown"] = lambda text: markdown.markdown(text, extensions=['extra', 'codehilite'])

posts = []
for filename in POSTS_DIR.iterdir():
    if filename.suffix == ".md":
        filepath = POSTS_DIR/filename
        post = frontmatter.load(filepath)
        slug = post.get('slug', filename.stem.replace(' ', '-').lower())
        date = post.get('date')
        content_html = markdown.markdown(post.content, extensions=['extra', 'codehilite'])

        posts.append({
            'title': post.get('title', '无标题'),
            'date': date,
            'slug': slug,
            'content': content_html,
        })
    posts.sort(key=lambda x: x['date'], reverse=True)


for post in posts:
    post_html = env.get_template("post.html").render(post=post, posts=posts)
    out_path = OUTPUT_DIR/f"{post['slug']}.html"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(post_html)

index_html = env.get_template("index.html").render(posts=posts)
with open(OUTPUT_DIR/"index.html", 'w', encoding='utf-8') as f:
    f.write(index_html)
