import json

import pydocparser

pydocparser.set('json_friendly', True)
parser = pydocparser.ModuleParser(pydocparser)
output = parser.start()

print(json.dumps(output, indent=4, sort_keys=True))
