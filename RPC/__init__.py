__version__ : str = '0.0.1'
__date_deploy__ : str = '20220922'
__json_rpc_version__ : str = '2.0'

# FIXME :trocar depois
class ExceptionZero(Exception):
    '''Exception gerenciada'''
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

# class ExceptionZeroClose(ExceptionZero):
#     '''Exception gerenciada'''
#     def __init__(self, *args, **kwargs):
#         ExceptionZero.__init__(self, *args, **kwargs)

class ExceptionZeroErro(ExceptionZero):
    '''Exception gerenciada'''
    def __init__(self, *args, **kwargs):
        ExceptionZero.__init__(self, *args, **kwargs)

# ref: https://www.jsonrpc.org/specification#error_object
# -32000 to -32099	Server error	Reserved for implementation-defined server-errors.
class ExceptionZeroRPC(ExceptionZero):
    '''Exception gerenciada'''
    def __init__(self, *args, **kwargs):
        ExceptionZero.__init__(self, *args, **kwargs)
