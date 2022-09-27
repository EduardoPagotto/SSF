__version__ : str = '1.0.0'
__date_deploy__ : str = '20220927'
__json_rpc_version__ : str = '2.0'

# ref: https://www.jsonrpc.org/specification#error_object
# -32000 to -32099	Server error	Reserved for implementation-defined server-errors.
class ExceptionRPC(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)