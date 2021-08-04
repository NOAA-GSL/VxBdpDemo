import sys
import click
import boto3

from bdp_demo import storage_layer
from bdp_demo import handlers
from bdp_demo import log


@click.command()
@click.argument("s3_uri")
def bdp_demo(s3_uri) -> int:
    """Grab the resource at S3_URI and print it.

    S3_URI should should take the form "s3://bucket/key"
    """
    # Initialize the S3 storage layer
    s3_client = boto3.client("s3")
    s3 = storage_layer.S3Storage(s3_client)

    # Initialize file handlers
    text = handlers.TextHandler(sys.stdout)
    # tar = storage_layer.TarHandler(sys.stdout)
    # grib2 = storage_layer.Grib2Handler(sys.stdout)

    logger = log.Logger(s3, [text])

    logger.log(s3_uri)

    return 0
