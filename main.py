#!/usr/bin/env python3
import os
import shutil
import markdown
from jinja2 import Environment, FileSystemLoader
import frontmatter

# 配置
POSTS_DIR = "posts"
TEMPLATES_DIR = "templates"
OUTPUT_DIR = "dist"
STATIC_DIR = "static"   # 可选，如有静态文件则复制

def build():
    # 1. 清空并重建输出目录
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    # 2. 复制静态文件（如 style.css）
    if os.path.exists(STATIC_DIR):
        dest = os.path.join(OUTPUT_DIR, os.path.basename(STATIC_DIR))
        shutil.copytree(STATIC_DIR, dest)

    # 3. 加载 Jinja2 模板
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    # 为了让模板能使用 markdown 过滤器，可以注册一个自定义过滤器
    env.filters["markdown"] = lambda text: markdown.markdown(text, extensions=['extra', 'codehilite'])

    # 4. 读取所有文章
    posts = []
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(POSTS_DIR, filename)
            post = frontmatter.load(filepath)
            # 处理元数据：标题、日期、slug等
            slug = post.get('slug', filename[:-3].replace(' ', '-').lower())
            date = post.get('date')
            # 将 Markdown 内容转为 HTML
            content_html = markdown.markdown(post.content, extensions=['extra', 'codehilite'])

            posts.append({
                'title': post.get('title', '无标题'),
                'date': date,
                'slug': slug,
                'content': content_html,
            })
        # 按日期排序（假设 front matter 里有 date 字段，格式 YYYY-MM-DD）
        posts.sort(key=lambda x: x['date'], reverse=True)

    # 5. 生成每篇文章的独立页面
    for post in posts:
        html = env.get_template("post.html").render(post=post, posts=posts)
        out_path = os.path.join(OUTPUT_DIR, f"{post['slug']}.html")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)

    # 6. 生成首页（列出所有文章）
    index_html = env.get_template("index.html").render(posts=posts)
    with open(os.path.join(OUTPUT_DIR, "index.html"), 'w', encoding='utf-8') as f:
        f.write(index_html)

    print(f"✅ 成功生成 {len(posts)} 篇文章，输出目录：{OUTPUT_DIR}")

if __name__ == "__main__":
    build()