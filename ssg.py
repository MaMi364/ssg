import markdown
from jinja2 import Template
import frontmatter
import os


def ProcessMDfile(file,type):
    fm = frontmatter.loads(file)
    file = fm.content
    html_content = markdown.markdown(file)

    with open(f"templates/{type}_template.html", "r") as f:
        html_template = f.read()

    template = Template(html_template)

    if type == "pages" or type == "page":
        rendered_template = template.render(
            title=fm['title'],
            navigation=fm['navigation'],
            year=fm['year'],
            site_name=fm['site_name'],
            content=html_content
        )

    elif type == "posts" or type == "post":
        rendered_template = template.render(
            title=fm['title'],
            author=fm['author'],
            date=fm['date'],
            navigation=fm['navigation'],
            year=fm['year'],
            site_name=fm['site_name'],
            content=html_content
        )

    subfolder = "_site"
    file_number = 1

    # Als file bestaat increment met 1 tot hij komt tot een naam dat niet bestaat
    while True:
        new_filename = f"{type}_{file_number}.html"
        filepath = os.path.join(subfolder, new_filename)

        if not os.path.exists(filepath):
                break
        file_number += 1
    with open(filepath, "w") as f:
        f.write(rendered_template)

def readAllFiles(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                if folder=="pages": 
                    type="page"
                elif folder=="posts":
                    type="post"
                ProcessMDfile(content, type)


readAllFiles("pages")
readAllFiles("posts")
print("Je hebt onze SSG gebruikt om pages en posts te creeren")

