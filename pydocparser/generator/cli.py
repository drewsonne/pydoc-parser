import click
from jinja2 import Template

import pydocparser


@click.command()
@click.argument('module_name')
def markdown(module_name):
    parser = pydocparser.ModuleParser(module_name)
    structure = parser.start()

    template = Template(MARKDOWN_TEMPLATE)

    def template_function(func):
        template.globals[func.__name__] = func
        return func



    click.echo(template.render(struct=structure, module_name=module_name))


MARKDOWN_TEMPLATE = """# {{ struct.name }}
{{ struct.doc }}

## API
### Classes
{% for class in struct.classes %}
#### {{ class.name }}({% for super in class.superclasses %}[{{ super }}](#{{ super | replace('.','') | lower() }}){% endfor %})
{{ class.doc }}
{% for method in class.methods %}
##### {{ method.name | replace(class.name~".","") | replace("_","\_") }}{{ method.sig }}
{% endfor %}
{% endfor %}
{% for module in struct.modules %}
{% for class in module.classes %}
#### {{ class.name }}
{% endfor %}
{% endfor %}
### Functions
{% for function in struct.functions %}
#### {{ function.name }}
{{ function.doc }}
{% endfor %}

"""
