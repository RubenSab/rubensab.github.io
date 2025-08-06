import os
import sys
import markdown
import yaml
import re

HELP = """
Usage:
    editor.py add <title>
    editor.py remove <post_id>
    editor.py gallery add <title>
    editor.py gallery remove <post_id>

Commands:
    add, a           Add a new .md post using the given title.
    remove, r        Remove an existing post by its ID.
    gallery add, ga  Add a new .md gallery item using the given title.
    gallery remove, gr Remove an existing gallery item by its ID.

Examples:
    python editor.py add "new_post.md"
    python editor.py remove 123
    python editor.py gallery add "new_artwork.md"
    python editor.py gallery remove 456

Errors:
    - Raises ValueError if arguments are missing or invalid.
"""


# Function to convert .md source file into HTML content for single post/gallery item and preview
def md_to_html(source_file_name, is_gallery=False):
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

    # Determine paths and class names based on whether it's a gallery item
    if is_gallery:
        back_link = '../gallery.html'
        back_text = '&lt;&lt; Gallery'
        article_class = 'single-post'
        folder_name = 'gallery'
        index_file = 'gallery.html'
    else:
        back_link = '../index.html'
        back_text = '&lt;&lt; Home'
        article_class = 'single-post'
        folder_name = 'posts'
        index_file = 'index.html'

    # Create the single-post/gallery-item HTML
    html_single_item = (
        f'<article class="{article_class}">\n'
        f'    <a href="{back_link}" class="back-link">{back_text}</a>\n'
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

    # Create a preview for the item on the homepage/gallery page
    text_preview = md_content.strip().strip('#').replace('\n', ' ')[:138] + '...'

    html_item_preview = (
        f'<div class="post">\n'
        f'    <a href="{folder_name}/{post_id}.html">\n'
        f'        <img alt="thumbnail of {"artwork" if is_gallery else "post"} {post_id}" src="thumbnails/{thumbnail}">\n'
        f'    </a>\n'
        f'    <div class="post-header">\n'
        f'        <h1 class="post-title">\n'
        f'            <a href="{folder_name}/{post_id}.html">{title}</a>\n'
        f'        </h1>\n'
        f'        <span class="post-id">#{post_id}</span>\n'
        f'    </div>\n'
        f'    <p>\n'
        f'        {text_preview}\n'
        f'    </p>\n'
        f'    <span class="post-date">{date}</span>\n'
        f'</div>\n'
        f'<hr>\n'
    )

    return html_single_item, html_item_preview, title, date, post_id, thumbnail


# Function to add a post/gallery item to the appropriate folder and update the index
def add_item(source_file_name, is_gallery=False):
    source_folder = "gallery_source" if is_gallery else "source"
    output_folder = "gallery" if is_gallery else "posts"
    index_file = "gallery.html" if is_gallery else "index.html"

    html_single_item, html_item_preview, title, date, post_id, thumbnail = md_to_html(
        f"{source_folder}/{source_file_name}", is_gallery)
    output_file_name = f"{output_folder}/{post_id}.html"

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Write the item's full HTML to a new file
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
            f'        {html_single_item}\n'
            f'    </div>\n'
            f'</body>\n'
            f'</html>\n'
        )

    print(f"{output_file_name} written correctly")

    # Update the appropriate index file with the item preview
    with open(index_file, "r+") as f:
        content = f.read()
        content = content.replace("<!-- NEXT POST -->",
                                  f'<!-- NEXT POST -->\n'
                                  f'\n'
                                  f'<!-- {post_id} -->\n'
                                  f'{html_item_preview}'
                                  f'<!-- END -->\n'
                                  )
        f.seek(0)
        f.write(content)
        f.truncate()

    print(f"{index_file} updated correctly")


# Legacy function for backward compatibility
def add_post(source_file_name):
    add_item(source_file_name, is_gallery=False)


# Function to remove a post/gallery item (delete from index and remove the file)
def remove_item(post_id, is_gallery=False):
    output_folder = "gallery" if is_gallery else "posts"
    index_file = "gallery.html" if is_gallery else "index.html"

    # Remove the item from the appropriate index file
    with open(index_file, "r+") as f:
        content = f.read()

    # Create a pattern to search for the item preview block
    item_preview_pattern = f'<!-- {post_id} -->\n.*?<!-- END -->'

    # Replace the item block with an empty string
    new_content = re.sub(item_preview_pattern, '', content, flags=re.DOTALL)

    # Write the updated content to the index file
    with open(index_file, "w") as f:
        f.write(new_content)

    # Delete the item file from the appropriate folder
    item_file_path = f"{output_folder}/{post_id}.html"
    if os.path.exists(item_file_path):
        os.remove(item_file_path)
        print(f"File {item_file_path} removed successfully.")
    else:
        print(f"File {item_file_path} not found.")


# Legacy function for backward compatibility
def remove_post(post_id):
    remove_item(post_id, is_gallery=False)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in {'-h', '--help'}:
        print(HELP)
        return

    try:
        # Handle gallery commands
        if sys.argv[1] == 'gallery':
            if len(sys.argv) < 4:
                raise ValueError("Missing arguments for gallery command.")

            match sys.argv[2]:
                case 'a' | 'add':
                    add_item(sys.argv[3], is_gallery=True)
                case 'r' | 'remove':
                    remove_item(sys.argv[3], is_gallery=True)
                case _:
                    raise ValueError("Invalid gallery action.")
        else:
            # Handle regular post commands
            match sys.argv[1]:
                case 'a' | 'add':
                    add_post(sys.argv[2])  # add post from title
                case 'r' | 'remove':
                    remove_post(sys.argv[2])  # remove post from ID
                case _:
                    raise ValueError("Invalid action.")
    except IndexError:
        raise ValueError("Missing arguments. Check usage with --help")


if __name__ == "__main__":
    main()
