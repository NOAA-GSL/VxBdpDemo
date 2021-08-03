from bdp_demo import handlers

import pytest
import sys


# Arrange
@pytest.fixture
def text_handler():
    handler = handlers.TextHandler(sys.stdout)
    return handler


def test_text_handler_mtype(text_handler):
    """Test that we support text/plain mtypes"""
    assert text_handler.supports("text/plain")


def test_text_handler_mtype_fake(text_handler):
    """Test that we don't support fake mtypes"""
    assert not text_handler.supports("fake/mtype")


def test_text_handler_emit_stdout(capsys):
    """Test that we correctly emit a message to stdout"""
    # Act
    tst_str = "test string"
    th = handlers.TextHandler(sys.stdout)
    th.emit(tst_str.encode("utf-8"))
    stdout, stderr = capsys.readouterr()

    # Assert
    assert stdout == tst_str


def test_text_handler_emit_stderr(capsys):
    """Test that we correctly emit a message to stdout"""
    # Act
    tst_str = "test string"
    th = handlers.TextHandler(sys.stderr)
    th.emit(tst_str.encode("utf-8"))
    stdout, stderr = capsys.readouterr()

    # Assert
    assert stderr == tst_str


def test_text_handler_emit_stdout_fail(text_handler, capsys):
    """For some reason using the fixture version fails

    TODO. I'm guessing sys.stdout is somehow silently closed.
    """
    # Act
    tst_str = "test string"
    text_handler.emit(tst_str.encode("utf-8"))
    stdout, stderr = capsys.readouterr()

    # Assert
    assert not stdout == tst_str


def test_text_handler_emit_stdout_fixture(text_handler, capsys):
    """For some reason using the fixture version fails

    TODO. I'm guessing sys.stdout is somehow silently closed.
    """
    # Act
    tst_str = "test string"
    text_handler.output_file = sys.stdout  # TODO - this shouldn't be necessary...
    text_handler.emit(tst_str.encode("utf-8"))
    stdout, stderr = capsys.readouterr()

    # Assert
    assert stdout == tst_str


def test_supports_fn(text_handler):
    mtype = "text/plain"
    assert handlers.supports(text_handler, mtype)


def test_supports_fn_failure(text_handler):
    mtype = "foo/bar"
    assert not handlers.supports(text_handler, mtype)


def test_tar_handler_not_implemented():
    with pytest.raises(NotImplementedError):
        handlers.TarHandler(sys.stdout)


def test_grib2_handler_not_implemented():
    with pytest.raises(NotImplementedError):
        handlers.Grib2Handler(sys.stdout)
