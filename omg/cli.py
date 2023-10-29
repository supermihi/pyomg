import logging

import click


@click.group()
@click.option('-v', '--verbose', count=True)
@click.pass_context
def cli(ctx, verbose):
    ctx.obj = {}
    match verbose:
        case 0:
            log_level = logging.WARNING
        case 1:
            log_level = logging.INFO
        case _:
            log_level = logging.DEBUG
    logging.basicConfig(level=log_level)


def run():
    import omg.files.cli
    cli()
