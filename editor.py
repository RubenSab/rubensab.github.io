import markdown, sys

def export_html(input_file: str) -> None:
    date = input_file.split(".")[0]
    with open(input_file, "r", encoding="utf-8") as input_file:
        text = input_file.read()
    content = markdown.markdown(text)
    
    html = f"""
<!DOCTYPE html>
<html lang="it">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.00, maximum-scale=2.00, minimum-scale=1.00">
    <title>TITLE</title>
    <link rel="stylesheet" href="../../../style/base.css">
    <link rel="stylesheet" href="../../../style/post.css">
</head>

<body>
    <div class="container">
    	<a href="../../../index.html" class="back-link">{{ Go home }}</a>
		<div class="header">
	    	<div class="thumbnail">
	    		<img src="THUMBNAIL" alt="Thumbnail">
	    	</div>
	    	<div class="title"><h1>title</h1></div>
	    	<div class="date">{date}</div>
    	</div>
    	<div class="content">
    	{content}
    	</div>
    </body>
</html>
"""
    with open(date+".html", "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
        output_file.write(html)

if __name__ == "__main__":
    export_html(sys.argv[1])
