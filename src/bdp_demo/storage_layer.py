import os
import sys
import boto3
import botocore
from urllib.parse import urlparse
from typing import Optional, Iterator, TYPE_CHECKING

# Don't use boto3 stubs in production
if TYPE_CHECKING:
    from mypy_boto3_s3.service_resource import S3ServiceResource
else:
    S3ServiceResource = object


class S3Storage:
    def __init__(self) -> None:
        self.s3 = boto3.client("s3")

    def scheme(self) -> str:
        return "s3://"

    def supports(self, s3_uri) -> bool:
        return s3_uri.startswith(self.scheme())

    def error_check_resource(self, bucket, key):
        # Check if the bucket exists
        try:
            self.s3.head_bucket(Bucket=bucket)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                print(f"Error: Bucket not found - s3://{bucket}")
                sys.exit(1)
            elif e.response["Error"]["Code"] == "403":
                print(f"Error: Access denied to bucket - s3://{bucket}")
                sys.exit(1)
            else:
                # Something else went wrong
                raise

        # Check if the key exists
        try:
            self.s3.head_object(Bucket=bucket, Key=key)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                print(f"Error: Object not found - s3://{bucket}/{key}")
                sys.exit(1)
            elif e.response["Error"]["Code"] == "403":
                print(f"Error: Access denied to object - s3://{bucket}/{key}")
                sys.exit(1)
            else:
                # Something else went wrong
                raise

    def read(self, s3_uri) -> Iterator[bytes]:
        url_components = urlparse(s3_uri, allow_fragments=False)
        bucket = url_components.netloc
        key = url_components.path.lstrip("/")

        self.error_check_resource(bucket, key)

        response = self.s3.get_object(Bucket=bucket, Key=key)

        return response["Body"].iter_lines(keepends=True)

    def query_mime_type(self, s3_uri) -> str:
        """Get the MIME type S3 has for the object"""
        url_components = urlparse(s3_uri, allow_fragments=False)
        bucket = url_components.netloc
        key = url_components.path.lstrip("/")

        self.error_check_resource(bucket, key)

        response = self.s3.head_object(Bucket=bucket, Key=key)

        return response["ContentType"]

    def guess_mtype(self, s3_uri) -> Optional[str]:
        """Return a MIME type based on trivial MIME sniffing

        MIME sniffs based on the file ending. Returns None if it doesn't recognize
        the ending.
        """
        _, ending = os.path.splitext(s3_uri)
        mime_dict = {
            ".grib2": "application/x-grib2",  # Or "application/wmo-grib2"
            ".spec": "text/plain",
            ".bull": "text/plain",
            ".cbull": "text/plain",
            ".tar": "application/x-tar",
        }

        return mime_dict.get(ending)

    def get_mtype(self, s3_uri) -> str:
        _, ending = os.path.splitext(s3_uri)

        mtype = self.query_mime_type(s3_uri)

        # Try MIME Sniffing if we get a generic content type back
        if mtype == "binary/octet-stream":
            mime_sniff = self.guess_mtype(s3_uri)
            if mime_sniff is not None:
                mtype = mime_sniff
        return mtype

    def download(self, s3_uri) -> None:
        url_components = urlparse(s3_uri, allow_fragments=False)
        bucket = url_components.netloc
        key = url_components.path.lstrip("/")

        self.error_check_resource(bucket, key)

        self.s3.download_file(Bucket=bucket, Key=key, Filename=os.path.basename(key))


class FileStorage:
    def __init__(self) -> None:
        raise NotImplementedError
