from bdp_demo import log
from bdp_demo import storage_layer
from bdp_demo import handlers

import pytest
import sys


# Arrange
@pytest.fixture
def logger():
    # TODO: decouple this
    handler = handlers.TextHandler(sys.stdout)
    s3 = storage_layer.S3Storage()  # TODO - use a FileStorage instead?
    logger = log.Logger(storage_layer=s3, handlers=[handler])
    return logger


def test_log_bad_resource(logger):
    with pytest.raises(SystemExit):
        logger.log("s3://foo/bar.baz")


def test_log_unsupported_storage(logger):
    with pytest.raises(SystemExit):
        logger.log("foo://bar.baz")

# TODO - actually test the logger
