import requests
from typing import List
from pathlib import Path
from multiprocessing import Pool, cpu_count
from functools import partial

from models.instagram import Post, Paging
from utils.iso import to_filename

USER_MEDIA_URL = "https://graph.instagram.com/me/media?fields=id,caption,media_url,media_type,timestamp,children{id,media_url}"

DEFAULT_PAGE_LIMIT = 25
MAX_PAGE_LIMIT = 100


def query_string(access_token, paging: Paging = None, limit: int = DEFAULT_PAGE_LIMIT):
    params = {"access_token": access_token, "limit": min(limit, MAX_PAGE_LIMIT)}

    if isinstance(paging, Paging) and paging.has_next_cursor():
        return {**params, "after": paging.cursors.after}

    return params


def fetch(access_token, paging: Paging = None, limit: int = DEFAULT_PAGE_LIMIT):
    response = requests.get(
        USER_MEDIA_URL, params=query_string(access_token, paging, limit)
    )
    response.raise_for_status()

    content = response.json()
    posts = content["data"]

    list = []

    for post in posts:
        if "media_type" in post and (
            post["media_type"] == "IMAGE" or post["media_type"] == "CAROUSEL_ALBUM"
        ):
            list.append(Post(post))

    paging = Paging(content["paging"]) if "paging" in content else None

    return (list, paging)


def download_image(post: Post, output):
    filename = f"{to_filename(post.timestamp)}_{post.id}"
    local_path = Path(output, filename).with_suffix(".jpg")

    print(f"Downloading '{post.media_url}'...")
    media = requests.get(post.media_url)

    with open(local_path, "wb") as file:
        file.write(media.content)
    print(f"Download completed for '{local_path}'")


def download_media(posts: List[Post], output):
    print(f"Downloading {len(posts)} media.")

    pool = Pool(cpu_count())
    download_func = partial(download_image, output=output)
    pool.map(download_func, posts)
    pool.close()
    pool.join()
