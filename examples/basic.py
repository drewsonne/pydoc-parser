import json

import pydocparser

pydocparser.set('json_friendly', True)
parser = pydocparser.ModuleParser(pydocparser)

print(json.dumps(parser.start(), indent=4, sort_keys=True))
