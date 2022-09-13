import os
import click

from api.instagram import fetch, download_media


@click.group(invoke_without_command=True)
def cli():
    pass


@cli.command()
@click.option("-o", "--output", type=click.Path(), default=".")
@click.argument("access_token")
def list(output, access_token):
    posts = fetch(access_token)

    if not os.path.exists(output):
        os.makedirs(output, exist_ok=True)

    download_media(posts, output)
