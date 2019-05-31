class Mail(object):
    def __init__(self, **kwargs):
        for field in ('to', 'name', 'owner', 'status'):
            setattr(self, field, kwargs.get(field, None))