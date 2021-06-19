class MalformedRequest(Exception):
    def __init__(self, msg):
        super(MalformedRequest, self).__init__(msg)


class NotFound(Exception):
    def __init__(self, msg=None):
        super(NotFound, self).__init__(msg)


class ServiceNotAvailable(Exception):
    def __init__(self, msg=None):
        super(ServiceNotAvailable, self).__init__(msg)

