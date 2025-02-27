class Link:

    def __init__(self, source, target, **kwargs):
        self.source = source
        self.target = target
        self.__dict__.update(**kwargs)

    def to_dict(self):
        return self.__dict__
