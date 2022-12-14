from datetime import datetime
from turtle import pos
import requests
from typing import List
from pathlib import Path
from multiprocessing import Pool, cpu_count
from functools import partial

from models.instagram import Post, Paging
from utils.iso import to_filename
from utils.templates import grid_template, save_template

USER_MEDIA_URL = "https://graph.instagram.com/me/media?fields=id,caption,media_url,media_type,timestamp,children{id,media_url}"

DEFAULT_PAGE_LIMIT = 25
MAX_PAGE_LIMIT = 100


def filter_posts(posts: List[Post], greater_than: datetime = None) -> List[Post]:
    if greater_than is not None:
        return list(
            filter(
                lambda post: post.get_offset_naive_timestamp() >= greater_than, posts
            )
        )
    return posts


def query_string(access_token, paging: Paging = None, limit: int = DEFAULT_PAGE_LIMIT):
    params = {"access_token": access_token, "limit": min(limit, MAX_PAGE_LIMIT)}

    if isinstance(paging, Paging) and paging.has_next_cursor():
        return {**params, "after": paging.cursors.after}

    return params


def fetch_media(
    access_token,
    paging: Paging = None,
    greater_than: datetime = None,
    limit: int = DEFAULT_PAGE_LIMIT,
):
    print(f"Fetching user media '{USER_MEDIA_URL}' ...")
    response = requests.get(
        USER_MEDIA_URL, params=query_string(access_token, paging, limit)
    )
    response.raise_for_status()
    print(f"User media '{USER_MEDIA_URL}' fecthed")

    content = response.json()
    posts = content["data"]

    list = []

    for post in posts:
        if "media_type" in post and (
            post["media_type"] == "IMAGE" or post["media_type"] == "CAROUSEL_ALBUM"
        ):
            list.append(Post(post))

    list = filter_posts(list, greater_than)

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


def list_all(
    access_token, greater_than: datetime = None, limit: int = DEFAULT_PAGE_LIMIT
):
    all_posts: List[Post] = []
    current_paging = None

    posts, paging = fetch_media(access_token, greater_than=greater_than, limit=limit)
    all_posts.extend(posts)
    current_paging = paging
    paging_count = 1

    while current_paging is not None and current_paging.has_next_cursor():
        posts, paging = fetch_media(
            access_token, paging=current_paging, greater_than=greater_than, limit=limit
        )
        all_posts.extend(posts)
        current_paging = paging
        paging_count += 1

    return (all_posts, paging_count)


def download_all(
    access_token, output, greater_than: datetime = None, limit: int = DEFAULT_PAGE_LIMIT
) -> List[Post]:
    all_posts: List[Post] = []
    current_paging = None

    posts, paging = fetch_media(access_token, greater_than=greater_than, limit=limit)
    all_posts.extend(posts)
    current_paging = paging
    download_media(posts, output)

    while current_paging is not None and current_paging.has_next_cursor():
        posts, paging = fetch_media(
            access_token, paging=current_paging, greater_than=greater_than, limit=limit
        )
        all_posts.extend(posts)
        current_paging = paging
        download_media(posts, output)

    return all_posts


def save_page(all_posts: List[Post], output):
    save_template(output, "all_posts", grid_template(all_posts))
