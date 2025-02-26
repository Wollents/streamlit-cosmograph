class Link:

    def __init__(self, source, target):
        self.source = source
        self.target = target

    def to_dict(self):
        return self.__dict__
