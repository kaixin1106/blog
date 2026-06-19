from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import markdown
from markdown.extensions.toc import TocExtension
import frontmatter
import shutil

root_path = Path.cwd()
OUTPUT_DIR = root_path/"dist"
POSTS_DIR = root_path/"posts"
TEMPLATES_DIR = root_path/"templates"

if not OUTPUT_DIR.exists():
    OUTPUT_DIR.mkdir()

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# --- 读取文章 ---
posts = []
for filename in POSTS_DIR.iterdir():
    if filename.suffix == ".md":
        filepath = POSTS_DIR/filename
        post = frontmatter.load(filepath)
        slug = post.get('slug', filename.stem.replace(' ', '-').lower())
        date = post.get('date')

        # 使用 TocExtension 生成目录
        md = markdown.Markdown(
            extensions=['extra', 'codehilite', TocExtension(permalink=False, baselevel=2)]
        )
        content_html = md.convert(post.content)
        toc_html = md.toc

        tags = post.get('tags', [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(',') if t.strip()]

        posts.append({
            'title': post.get('title', '无标题'),
            'date': date,
            'slug': slug,
            'content': content_html,
            'toc': toc_html,
            'tags': tags,
        })
posts.sort(key=lambda x: x['date'], reverse=True)

# --- 读取时间线 ---
timeline = []
timeline_path = root_path/"timeline.md"
if timeline_path.exists():
    tl_data = frontmatter.load(timeline_path)
    for item in tl_data.get('events', []):
        timeline.append({
            'date': item.get('date', ''),
            'text': item.get('text', ''),
        })

# --- 渲染文章页面 ---
for post in posts:
    post_html = env.get_template("post.html").render(
        post=post, posts=posts, timeline=timeline
    )
    out_path = OUTPUT_DIR/f"{post['slug']}.html"
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(post_html)

# --- 渲染首页 ---
index_html = env.get_template("index.html").render(posts=posts, timeline=timeline)
with open(OUTPUT_DIR/"index.html", 'w', encoding='utf-8') as f:
    f.write(index_html)

# --- 复制 CSS ---
for file in TEMPLATES_DIR.iterdir():
    if file.suffix == ".css":
        shutil.copy2(file, OUTPUT_DIR/file.name)
