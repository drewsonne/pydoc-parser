import re


class DocParser(object):
    def __init__(self, docblock):
        self._block = docblock

    def start(self):
        if self._block is None:
            return {}
        lines = self._block.split("\n")
        description = []
        current_key = ''
        current_args = ''
        current_value = ''
        doc = {}
        for line in lines:

            matches = re.match(":(?P<key>[^\s]+)(?:\s*(?P<args>[^:]*)):(?:\s*(?P<description>.*))", line)
            if matches is not None:
                matches = matches.groupdict()

            if current_key == '':
                if line.startswith(':'):
                    current_key = matches['key']
                    current_args = matches['args']
                else:
                    current_key = 'description'

            if current_key == 'description':
                if line == '':
                    current_key = ''
                    continue
                if 'description' not in doc:
                    doc['description'] = []
                doc['description'].append(line)
                continue

            if (current_key == matches['key']) and (current_args == matches['args']):
                current_key = matches['key']
                current_args = matches['args']
                current_value += matches['description']
            else:
                if current_key == 'description':
                    doc['description'] = "\n".join(doc['description'])
                    continue
                if current_key not in doc:
                    doc[current_key] = {}
                if current_args not in doc[current_key]:
                    doc[current_key][current_args] = current_value
                doc[current_key][current_args] = '\n'.join(doc[current_key][current_args])
                current_key = matches['key']
                current_args = matches['args']
                current_value = matches['description']

        if current_key != 'description':
            if current_key not in doc:
                doc[current_key] = {}
            if current_args not in doc[current_key]:
                doc[current_key][current_args] = current_value
            doc[current_key][current_args] = '\n'.join(doc[current_key][current_args])

        return doc
