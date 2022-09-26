__version__ : str = '0.0.1'
__date_deploy__ : str = '20220926'
__json_rpc_version__ : str = '2.0'

# ref: https://www.jsonrpc.org/specification#error_object
# -32000 to -32099	Server error	Reserved for implementation-defined server-errors.
class ExceptionRPC(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)