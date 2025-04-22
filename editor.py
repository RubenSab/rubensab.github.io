import os
import sys
import markdown
import yaml
import re
import textwrap

# Function to convert .md source file into HTML content for single post and preview
def md_to_html(source_file_name):

    # Read .md source
    with open(source_file_name, "r") as f:
        raw_content = f.read()

    # Extract YAML metadata
    match = re.match(r"^---\n(.*?)\n---\n(.*)", raw_content, re.DOTALL)
    if match:
        metadata = yaml.safe_load(match.group(1))
        md_content = match.group(2)
    else:
        metadata = {}
        md_content = raw_content

    # Extract title, date, post_id, and thumbnail from metadata
    if "title" not in metadata:
        raise ValueError("TITLE MISSING!")
    if "date" not in metadata:
        raise ValueError("DATE MISSING!")
    if "id" not in metadata:
        raise ValueError("ID MISSING!")
    if "img" not in metadata:
        raise ValueError("THUMBNAIL MISSING!")

    title = metadata["title"]
    date = metadata["date"]
    post_id = metadata["id"]
    thumbnail = metadata["img"]

    # Convert markdown content to HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['fenced_code', 'codehilite'],
        extension_configs={
            'codehilite': {
                'linenums': False,
                'guess_lang': False,
                'pygments_style': 'github-dark',
                'noclasses': False
            }
        }
    )

    # Create the single-post HTML
    html_single_post = (
        f'<article class="single-post">\n'
        f'    <a href="../index.html" class="back-link">&lt;&lt; Home</a>\n'
        f'    <img src="../thumbnails/{thumbnail}" alt="Thumbnail">\n'
        f'    <div class="post-header">\n'
        f'        <h1>{title}</h1>\n'
        f'        <span class="post-id">#{post_id}</span>\n'
        f'    </div>\n'
        f'    <span class="post-date">{date}</span>\n'
        f'    <div class="post-content">\n'
        f'        {html_content}\n'
        f'    </div>\n'
        f'</article>\n'
    )

    # Create a preview for the post on the homepage
    text_preview = md_content.strip().strip('#').replace('\n', ' ')[:138] + '...'

    html_post_preview = (
        f'<div class="post">\n'
        f'    <a href="posts/{post_id}.html">\n'
        f'        <img alt="thumbnail of post {post_id}" src="thumbnails/{thumbnail}">\n'
        f'    </a>\n'
        f'    <div class="post-header">\n'
        f'        <h1 class="post-title">\n'
        f'            <a href="posts/{post_id}.html">{title}</a>\n'
        f'        </h1>\n'
        f'        <span class="post-id">#{post_id}</span>\n'
        f'    </div>\n'
        f'    <p>\n'
        f'        {text_preview}\n'
        f'    </p>\n'
        f'    <span class="post-date">{date}</span>\n'
        f'</div>\n'
    )

    return html_single_post, html_post_preview, title, date, post_id, thumbnail

# Function to add a post to the 'posts' folder and update 'index.html' with the preview
def add_post(source_file_name):
    html_single_post, html_post_preview, title, date, post_id, thumbnail = md_to_html(f"source/{source_file_name}")
    output_file_name = f"posts/{post_id}.html"

    # Write the post's full HTML to a new file
    with open(output_file_name, "w") as f:
        f.write(
            f'<!DOCTYPE html>\n'
            f'<html lang="it">\n'
            f'\n'
            f'<head>\n'
            f'    <meta charset="UTF-8">\n'
            f'    <meta name="viewport" content="width=device-width, initial-scale=1.00, maximum-scale=2.00, minimum-scale=1.00">\n'
            f'    <title>{title}</title>\n'
            f'    <link rel="stylesheet" href="../style.css">\n'
            f'    <link rel="stylesheet" href="../pygments.css">\n'        
            f'</head>\n'
            f'\n'
            f'<body>\n'
            f'    <div class="container">\n'
            f'        {html_single_post}\n'
            f'    </div>\n'
            f'</body>\n'
            f'</html>\n'
        )

    print(f"{output_file_name} written correctly")

    # Update index.html with the post preview
    with open("index.html", "r+") as f:
        content = f.read()
        content = content.replace("<!-- NEXT POST -->",
            f'<!-- NEXT POST -->\n'
            f'\n'
            f'<!-- {post_id} -->\n'
            f'{html_post_preview}'
            f'<!-- END -->\n'
        )
        f.seek(0)
        f.write(content)
        f.truncate()

    print("index.html updated correctly")

# Function to remove a post (delete from index.html and remove the post file)
def remove_post(post_id):
    # Remove the post from index.html
    with open("index.html", "r+") as f:
        content = f.read()

    # Create a pattern to search for the post preview block
    post_preview_pattern = f'<!-- {post_id} -->\n.*?<!-- END -->'
    
    # Replace the post block with an empty string
    new_content = re.sub(post_preview_pattern, '', content, flags=re.DOTALL)

    # Write the updated content to index.html
    with open("index.html", "w") as f:
        f.write(new_content)

    # Delete the post file from the 'posts' folder
    post_file_path = f"posts/{post_id}.html"
    if os.path.exists(post_file_path):
        os.remove(post_file_path)
        print(f"File {post_file_path} removed successfully.")
    else:
        print(f"File {post_file_path} not found.")


def main():
    try:
        match sys.argv[1]:
            case 'a' | 'add':
                add_post(sys.argv[2]) # add post from title
            case 'r' | 'remove':
                remove_post(sys.argv[2]) # remove post from ID
            case _:
                raise ValueError("Invalid action.")
    except IndexError:
        raise ValueError("Missing arguments. Usage: editor.py [add|remove] [value]")

if __name__ == "__main__":
    main()
