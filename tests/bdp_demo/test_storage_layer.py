from bdp_demo import storage_layer


def test_scheme():
    s3 = storage_layer.S3Storage()
    assert s3.scheme() == "s3://"


def test_supports():
    s3 = storage_layer.S3Storage()
    assert s3.supports("s3://")


def test_supports_fail():
    s3 = storage_layer.S3Storage()
    assert not s3.supports("file://")


def test_guess_mtype_grib2():
    s3 = storage_layer.S3Storage()
    assert s3.guess_mtype("s3://foo/bar.grib2") == "application/x-grib2"


def test_guess_mtype_spec():
    s3 = storage_layer.S3Storage()
    assert s3.guess_mtype("s3://foo/bar.spec") == "text/plain"


def test_guess_mtype_bull():
    s3 = storage_layer.S3Storage()
    assert s3.guess_mtype("s3://foo/bar.bull") == "text/plain"


def test_guess_mtype_cbull():
    s3 = storage_layer.S3Storage()
    assert s3.guess_mtype("s3://foo/bar.cbull") == "text/plain"


def test_guess_mtype_tar():
    s3 = storage_layer.S3Storage()
    assert s3.guess_mtype("s3://foo/bar.tar") == "application/x-tar"


def test_guess_mtype_unknown():
    s3 = storage_layer.S3Storage()
    assert s3.guess_mtype("s3://foo/bar.baz") is None


# TODO - mocks for check_resource_exists, read, query_mime_type, get_mtype and download
