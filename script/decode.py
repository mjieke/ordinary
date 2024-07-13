import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

root = "../src"
book = epub.read_epub("book.epub")

print(type(book), dir(book))
# 'add_author', 'add_item', 'add_metadata', 'add_prefix', 'bindings', 'direction',
#  'get_item_with_href', 'get_item_with_id', 'get_items', 'get_items_of_media_type',
# 'get_items_of_type', 'get_metadata', 'get_template', 'guide', 'items', 'language',
# 'metadata', 'namespaces', 'pages', 'prefixes', 'reset', 'set_cover', 'set_direction',
# 'set_identifier', 'set_language', 'set_template', 'set_title', 'set_unique_metadata',
#  'spine', 'templates', 'title', 'toc', 'uid', 'version']
print(dir(ebooklib))
# EXTENSIONS', 'ITEM_AUDIO', 'ITEM_COVER',
# 'ITEM_DOCUMENT', 'ITEM_FONT', 'ITEM_IMAGE', 'ITEM_NAVIGATION',
#  'ITEM_SCRIPT', 'ITEM_SMIL', 'ITEM_STYLE', 'ITEM_UNKNOWN',
#  'ITEM_VECTOR', 'ITEM_VIDEO', 'VERSION',
print(book.version, book.uid, book.title)

# 目录
tocs = []
for idx, t in enumerate(book.toc):
    # 'href', 'title', 'uid']
    print(type(t), t.title, len(book.toc))
    tocs.append(t.title)

with open(os.path.join(root, "SUMMARY.md"), "w") as f:
    f.write("# Summary\n")
    for idx, toc in enumerate(tocs):
        idx += 1
        f.write(f"- [{toc}](./chapter_{idx}.md)\n")


def exact_p_tag(content):
    soup = BeautifulSoup(content, "lxml")

    title = soup.find_all("title")
    # print(title)

    p_list = soup.find_all("p")
    cs = []
    for p in p_list:
        c = p.text.strip()
        if len(c) == 0:
            continue
        cs.append(c)

    if len(cs) > 1:
        cs[0] = cs[0].replace("(本章免费)", "")
        cs[0] = f"<center>{cs[0]}</center>"
        cs.append(f"<center>本章完结</center>")
    return "\n\n".join(cs)


print(book.pages)
print(book.metadata)
print(book.guide)
# print(book.spine)
for idx, c in enumerate(book.items):
    idx += 1
    # 'book', 'content', 'file_name', 'get_content', 'get_id', 'get_name',
    #  'get_type', 'id', 'is_linear', 'manifest', 'media_type', 'set_content']
    # print(type(c), c.file_name, c.get_name(), c.get_id(), c.media_type, len(book.items))
    content = c.get_content()
    # print(type(content), dir(content))
    text = exact_p_tag(content)
    if len(text) < 3:
        break
    name = f"chapter_{idx}.md"
    with open(os.path.join(root, name), "w") as f:
        f.write(text)


# for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
#     print(image)

# for item in book.get_items():
#     if item.get_type() == ebooklib.ITEM_DOCUMENT:
#         print(dir(item))
#         name = item.get_name()
#         title = item.title
#         content = item.get_content()
#         print(f"Chapter: {name} {title} {content}")
