import click
from jinja2 import Template

import pydocparser


@click.command()
@click.argument('module_name')
def markdown(module_name):
    parser = pydocparser.ModuleParser(module_name)
    structure = parser.start()

    template = Template(MARKDOWN_TEMPLATE)
    click.echo(template.render(struct=structure, module_name=module_name))


MARKDOWN_TEMPLATE = """# {{ struct.name }}
{{ struct.doc.description | join("\n") }}

## API
### Classes
{% for class in struct.classes %}
#### {{ class.name }}({% for super in class.superclasses %}[{{ super }}](#{{ super | replace('.','') | lower() }}){% endfor %})
{{ class.doc.description | join("\n") }}
{% for method in class.methods %}
##### {{ method.name | replace(class.name~".","") | replace("_","\_") }}{{ method.sig }}
{% if method.doc.param is defined %}
| Name | Type | Description | Default |
|------|------|-------------|---------|{% for key, obj in method.doc.param.items() %}
| {{ key }} | | {{ obj }} | |{% endfor %}
{% endif %}
{% endfor %}
{% endfor %}
{% for module in struct.modules %}
{% for class in module.classes %}
#### {{ class.name }}
{% endfor %}
{% endfor %}
### Functions
{% for function in struct.functions %}
#### {{ function.name }}{{ function.sig }}
{{ function.doc.description | join("\n")}}
{% if function.doc.param is defined %}
| Name | Type | Description | Default |
|------|------|-------------|---------|{% endif %}
{% endfor %}

"""
