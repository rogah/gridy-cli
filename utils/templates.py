from typing import List
from string import Template
from pathlib import Path
from models.instagram import Post

HTML_PAGE = """
<html>
<head>
    <title>$title</title>
    <style>
      .grid {
        display: grid;
        grid-template-columns: 250px 250px 250px;
      }
      .post {
        margin: 5px;
      }
      .media {
        position: relative;
      }
      .info {
        box-sizing: border-box;
        display: none;
        position: absolute;
        top: 0;
        right: 0;
        color: #fff;
        padding: 15px;
        font-size: .7em;
      }
      .media,
      .info {
        width: 240px;
        height: 240px;
        overflow: hidden;
        background-color: rgba(0, 0, 0, 0.4);
      }
      .media img {
        height: 300px;
      }
      .media:hover .info {
        display: block;
      }
    </style>
</head>
<body>
    <h1>$title</h1>
    <div class="grid">
        $grid
    </div>
</body>
</html>
"""

HTML_GRID_CELL = """
<div class="post">
    <div class="media">
        <img src="$url" alt="$id" title="$caption" data-id="$id" data-timestamp="$timestamp" />
        <div class="info">
            <div><span>ID</span>: <strong>$id</strong></div>
            <div><span>Timestamp</span>: <strong>$timestamp</strong></div>
            <div><span>Caption</span>: <p>$caption</p></div>
        </div>
    </div>
</div>
"""


def grid_template(posts: List[Post]):
    title = f"All Posts: {len(posts)}"

    cells = []
    for post in posts:
        grid_cell = Template(HTML_GRID_CELL).substitute(
            {
                "url": post.media_url,
                "id": post.id,
                "caption": post.caption,
                "timestamp": post.timestamp,
            }
        )
        cells.append(grid_cell)

    return Template(HTML_PAGE).substitute(
        {
            "title": title,
            "grid": "".join(cells),
        }
    )


def save_template(basepath, basename, content):
    local_path = Path(basepath, basename).with_suffix(".html")
    with open(local_path, "w") as file:
        file.write(content)
