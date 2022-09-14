import os
import click

from api.instagram import fetch, download_media, DEFAULT_PAGE_LIMIT


@click.group(invoke_without_command=True)
def cli():
    pass


@cli.command()
@click.option("-o", "--output", type=click.Path(), default=".")
@click.option("-l", "--limit", type=int, default=DEFAULT_PAGE_LIMIT)
@click.argument("access_token")
def list(output, limit, access_token):
    if not os.path.exists(output):
        os.makedirs(output, exist_ok=True)

    current_paging = None

    posts, paging = fetch(access_token, limit=limit)
    current_paging = paging
    download_media(posts, output)

    while current_paging is not None and current_paging.has_next_cursor():
        posts, paging = fetch(access_token, current_paging, limit=limit)
        current_paging = paging
        download_media(posts, output)
