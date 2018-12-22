import json

import pydocparser

parser = pydocparser.ModuleParser(pydocparser)

print(json.dumps(parser.start(), indent=4, sort_keys=True))
