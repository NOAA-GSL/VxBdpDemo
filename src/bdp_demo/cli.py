import sys
import os

import click
import boto3
import botocore
from typing import Optional, TYPE_CHECKING

# Don't use boto3 stubs in production
if TYPE_CHECKING:
    from mypy_boto3_s3.service_resource import S3ServiceResource
else:
    S3ServiceResource = object


def init_s3() -> S3ServiceResource:
    """A function that grabs env config and returns a boto s3 client"""

    s3 = boto3.resource("s3")

    return s3


def get_mime_type(client: S3ServiceResource, bucket: str, key: str) -> str:
    """Get the MIME type S3 has for the object"""
    obj = client.Object(bucket, key)

    try:
        obj.load()
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            print(f"Error: Object not found - s3://{bucket}/{key}")
            sys.exit(1)
        elif e.response["Error"]["Code"] == "403":
            print(f"Error: Access denied - s3://{bucket}/{key}")
            sys.exit(1)
        else:
            # Something else went wrong
            raise

    return obj.content_type


def guess_mime(key: str) -> Optional[str]:
    """Guess ('Sniff') the MIME types for UFS STS v5&6 based on file ending"""

    # Reference for grib2 MIME type:
    # https://docs.opengeospatial.org/is/16-060r2/16-060r2.html#_correct_mime_type
    _, ending = os.path.splitext(key)
    mime_dict = {
        ".grib2": "application/x-grib2",  # Or "application/wmo-grib2"
        ".spec": "text/plain",
        ".bull": "text/plain",
        ".cbull": "text/plain",
        ".tar": "application/x-tar",
    }

    return mime_dict.get(ending)


def get_s3_contents(client: S3ServiceResource, bucket: str, key: str) -> bytes:
    """A function to grab an S3 object"""

    obj = client.Object(bucket, key)

    # Check if the key exists
    try:
        obj.load()
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            print(f"Error: Object not found - s3://{bucket}/{key}")
            sys.exit(1)
        elif e.response["Error"]["Code"] == "403":
            print(f"Error: Access denied - s3://{bucket}/{key}")
            sys.exit(1)
        else:
            # Something else went wrong
            raise
    body = obj.get()["Body"].read()

    return body


@click.command()
@click.option("--bucket", required=True, help="The AWS bucket to connect to")
@click.option("--key", required=True, help="The S3 key in that bucket to print")
def echo_s3_object(bucket: str, key: str) -> int:
    """A console script to grab an S3 object and echo it to stdout"""

    s3 = init_s3()
    mtype: Optional[str] = get_mime_type(s3, bucket, key)
    if mtype == "binary/octet-stream":
        # There's a chance the file wasn't uploaded with an mtype - try mime sniffing
        mtype = guess_mime(key)

    if mtype != "text/plain":
        print(
            f"Can access resource s3://{bucket}/{key}. However, it contains an "
            "unsupported mtype so we can't print it. We'll attempt to download it "
            "instead."
        )
        # TODO: Warning - this file is X size. Proceed? Y/n.
        s3.Bucket(bucket).download_file(Key=key, Filename=os.path.basename(key))
        sys.exit(1)

    try:
        print(get_s3_contents(s3, bucket, key).decode("utf-8"))
    except UnicodeDecodeError:
        print(f"Error - not a text file: s3://{bucket}/{key}")
        sys.exit(1)

    return 0


# if __name__ == "__main__":  # pragma: no cover
#     sys.exit()
