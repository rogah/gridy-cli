from typing import List
from shutil import rmtree
import os
import click

from models.instagram import Post

from api.instagram import (
    list_all,
    download_all,
    save_page,
    DEFAULT_PAGE_LIMIT,
)


@click.group(invoke_without_command=True)
def cli():
    pass


@cli.command()
@click.option("-l", "--limit", type=int, default=DEFAULT_PAGE_LIMIT)
@click.option(
    "-gt",
    "--greater-than",
    type=click.DateTime(formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]),
    default=None,
)
@click.argument("access_token")
def list(limit, greater_than, access_token):
    all_posts, paging_count = list_all(access_token, greater_than, limit)

    for post in all_posts:
        print(f"{post.media_type}: {post.media_url}")
    print(f"Total: {len(all_posts)}. Pages: {paging_count}")


@cli.command()
@click.option("-o", "--output", type=click.Path(), default=".")
@click.option("-l", "--limit", type=int, default=DEFAULT_PAGE_LIMIT)
@click.option(
    "-gt",
    "--greater-than",
    type=click.DateTime(formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"]),
    default=None,
)
@click.argument("access_token")
def download(output, limit, greater_than, access_token):
    if os.path.exists(output):
        rmtree(output, ignore_errors=False, onerror=None)

    if not os.path.exists(output):
        os.makedirs(output, exist_ok=True)

    all_posts = download_all(
        access_token, output, greater_than=greater_than, limit=limit
    )

    save_page(all_posts, output)
