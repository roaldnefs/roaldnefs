import feedparser
import time
import re
from os import path


def open_readme():
    directory = path.abspath(path.dirname(__file__))
    with open(path.join(directory, 'README.md'), encoding='utf-8') as f:
        readme = f.read()
    return readme

def write_readme(updated):
    directory = path.abspath(path.dirname(__file__))
    with open(path.join(directory, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(updated)

def modify_readme(readme, text, identifier=''):
    start_tag = f'{identifier}_START'
    end_tag = f'{identifier}_END'
    return re.sub(f'(?<=<!-- {start_tag} -->).*?(?=<!-- {end_tag} -->)', text, readme, flags=re.DOTALL)


def list_posts(feed):
    posts = []
    feed = feedparser.parse(feed)
    for entry in feed.entries:
        title = entry['title']
        link = entry['link']
        published = time.strftime('%Y-%m-%d', entry['published_parsed'])
        posts.append(f"- [{title}]({link}) ({published})")
    return '\n' + '\n'.join(posts) + '\n'


if __name__ == '__main__':
    posts = list_posts("https://roaldnefs.com/posts/index.xml")
    original = open_readme()
    updated = modify_readme(original, posts, identifier='BLOG')
    write_readme(updated)
