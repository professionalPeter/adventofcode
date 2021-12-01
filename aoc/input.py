class Input:
    def __init__(self, data):
        self._data = data
    @classmethod
    def from_data(cls, data):
        return cls(data)
    @classmethod
    def from_file(cls, filepath):
        with open(filepath) as file:
            return cls(file.read())
    def parse_ints(self):
        return [int(i) for i in self._data.split()]

