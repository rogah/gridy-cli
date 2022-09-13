import requests
import os
from pathlib import Path
from multiprocessing import Pool, cpu_count
from functools import partial

from models.instagram import Post

USER_MEDIA_URL = (
    "https://graph.instagram.com/me/media?fields=id,caption,media_url,media_type"
)


def fetch(access_token):
    response = requests.get(USER_MEDIA_URL, params={"access_token": access_token})
    response.raise_for_status()

    content = response.json()
    posts = content["data"]

    list = []

    for post in posts:
        if "media_type" in post and (
            post["media_type"] == "IMAGE" or post["media_type"] == "CAROUSEL_ALBUM"
        ):
            list.append(Post(post))
        # post_id = post["id"]
        # thumbnail_url = post["thumbnail_url"]
        # thumbnail = requests.get(thumbnail_url)
        # with open(post_id, "wb") as file:
        #     file.write(thumbnail.content)

    return list


def download_image(post, output):
    local_path = Path(output, post.id).with_suffix(".jpg")

    print(f"Downloading {post.media_url}...")
    media = requests.get(post.media_url)

    with open(local_path, "wb") as file:
        file.write(media.content)
    print(f"Download completed for {local_path}.")


def download_media(posts, output):
    print(f"Downloading {len(posts)} media.")

    pool = Pool(cpu_count())
    download_func = partial(download_image, output=output)
    pool.map(download_func, posts)
    pool.close()
    pool.join()
