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
    def get_data(self):
        return self._data.strip()
    def parse_ints(self, sep=None):
        return [int(i) for i in self._data.split(sep)]
    def parse_lines(self):
        return self._data.splitlines()
    def parse_records(self):
        return [record.splitlines() for record in self._data.split('\n\n')]

