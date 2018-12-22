class DocParser(object):
    def __init__(self, docblock):
        self._block = docblock

    def start(self):
        return self._block
