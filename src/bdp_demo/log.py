import sys

# import bdp_demo_refactor.handlers


# In our case it makes no sense to use multiple storage engines. Assume just one.
# We only want one handler but we don't know which we'll need
# For handlers - get file MIME type and select handler that advertises
# it can handle that mtype
class Logger:
    def __init__(self, storage_layer, handlers) -> None:
        self.storage_layer = storage_layer
        self.handlers = handlers

    def log(self, uri) -> None:
        """Read the given uri and decode it with an appropriate handler

        log uses the given storage_layer to read the URI
        """
        # Test that our storage layer supports this file
        if not self.storage_layer.supports(uri):
            print(
                f"Error: No supported storage system for: {uri}\n"
                f"       Is the resource scheme missing? \n"
                f"       (Supported schemes are: {self.storage_layer.scheme()})"
            )
            sys.exit(1)

        mtype = self.storage_layer.get_mtype(uri)

        # Grab the first handler that supports the content at the uri
        handler = None
        for h in self.handlers:
            if h.supports(mtype):
                handler = h
                break
        if handler is None:
            print(
                f"Warning: No supported handler for detected file type: {mtype}\n"
                "Warning: Downloading file instead."
            )
            self.storage_layer.download(uri)
            sys.exit(1)

        # TODO - finish implementation
        # handler = filter(
        #     bdp_demo_refactor.handlers.supports(handler, mtype), self.handlers
        # )

        for line in self.storage_layer.read(uri):
            handler.emit(line)
