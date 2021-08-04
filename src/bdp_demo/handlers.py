from typing import Protocol


# Create a PEP 544 structural subtype to check our duck typing
class SupportsHandlerSupports(Protocol):  # pragma: no cover
    def supports(self, mtype: str) -> bool:
        ...


def supports(handler: SupportsHandlerSupports, mtype: str) -> bool:
    return handler.supports(mtype)


class TextHandler:
    """Reads bytestream, decodes to utf-8, and emits to a filehandle"""

    def __init__(self, output_file) -> None:
        self.output_file = output_file

    def supports(self, mtype: str) -> bool:
        return mtype == "text/plain"

    def emit(self, message: bytes) -> None:
        self.output_file.write(message.decode("utf-8"))
        self.output_file.flush()


class TarHandler:
    """Reads bytestream, decodes list of content, and emits to filehandle"""

    def __init__(self, output_file) -> None:
        raise NotImplementedError

    def supports(self, mtype: str) -> bool:
        raise NotImplementedError

    def emit(self, message: bytes) -> None:
        raise NotImplementedError


class Grib2Handler:
    """Reads bytestream, decodes first thing it finds(?), and emits to filehandle"""

    def __init__(self, output_file) -> None:
        raise NotImplementedError

    def supports(self, mtype: str) -> bool:
        raise NotImplementedError

    def emit(self, message: bytes) -> None:
        raise NotImplementedError
