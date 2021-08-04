from bdp_demo import storage_layer

import pytest
from botocore.stub import Stubber
import boto3


# Arrange
@pytest.fixture(scope="function")
def s3_client():
    s3 = boto3.client("s3")
    return s3


@pytest.fixture(scope="function")
def s3_stub(s3_client, autouse=True):
    with Stubber(s3_client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()


def test_scheme(s3_stub, s3_client):
    s3 = storage_layer.S3Storage(s3_client)
    assert s3.scheme() == "s3://"


def test_supports(s3_stub, s3_client):
    s3 = storage_layer.S3Storage(s3_client)
    assert s3.supports("s3://")


def test_supports_fail(s3_stub, s3_client):
    s3 = storage_layer.S3Storage(s3_client)
    assert not s3.supports("file://")


def test_guess_mtype_grib2(s3_stub, s3_client):
    s3 = storage_layer.S3Storage(s3_client)
    assert s3.guess_mtype("s3://foo/bar.grib2") == "application/x-grib2"


def test_guess_mtype_spec(s3_stub, s3_client):
    s3 = storage_layer.S3Storage(s3_client)
    assert s3.guess_mtype("s3://foo/bar.spec") == "text/plain"


def test_guess_mtype_bull(s3_stub, s3_client):
    s3 = storage_layer.S3Storage(s3_client)
    assert s3.guess_mtype("s3://foo/bar.bull") == "text/plain"


def test_guess_mtype_cbull(s3_stub, s3_client):
    s3 = storage_layer.S3Storage(s3_client)
    assert s3.guess_mtype("s3://foo/bar.cbull") == "text/plain"


def test_guess_mtype_tar(s3_stub, s3_client):
    s3 = storage_layer.S3Storage(s3_client)
    assert s3.guess_mtype("s3://foo/bar.tar") == "application/x-tar"


def test_guess_mtype_unknown(s3_stub, s3_client):
    s3 = storage_layer.S3Storage(s3_client)
    assert s3.guess_mtype("s3://foo/bar.baz") is None


# TODO - mocks for check_resource_exists, read, query_mime_type, get_mtype and download
