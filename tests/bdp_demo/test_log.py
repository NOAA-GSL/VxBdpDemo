from bdp_demo import log
from bdp_demo import storage_layer
from bdp_demo import handlers

import pytest
import sys
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


@pytest.fixture
def logger(s3_stub, s3_client):
    # TODO: decouple this
    handler = handlers.TextHandler(sys.stdout)
    s3 = storage_layer.S3Storage(s3_client)  # TODO - use a FileStorage instead?
    logger = log.Logger(storage_layer=s3, handlers=[handler])
    return logger


def test_log_bad_resource(logger, s3_stub):
    s3_stub.activate()
    # Mock checking for download
    s3_stub.add_response(
        "head_bucket",
        expected_params={"Bucket": "foo"},
        service_response={},
    )
    s3_stub.add_client_error(
        method="head_object",
        service_error_code="404",
        service_message="""
        The specified key does not exist.
        """,
    )
    with pytest.raises(SystemExit):
        logger.log("s3://foo/bar.baz")


def test_log_unsupported_storage(logger, s3_stub):
    with pytest.raises(SystemExit):
        logger.log("foo://bar.baz")


# TODO - actually test the logger
