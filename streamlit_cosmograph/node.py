class Node:
    def __init__(self, id, colors="#FDD2BS", label=None, x=None, y=None):
        self.id = id
        if label is None:
            self.label = str(id)
        else:
            self.label = label
        self.x = x
        self.y = y
        self.colors = colors

    def to_dict(self):
        return self.__dict__

    def __eq__(self, other) -> bool:
        return (isinstance(other, self.__class__) and
                getattr(other, 'id', None) == self.id)

    def __hash__(self) -> int:
        return hash(self.id)
