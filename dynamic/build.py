from jinja2 import Environment, FileSystemLoader
import yaml

env = Environment(loader=FileSystemLoader('templates'))
# Read yaml
with open("data/config.yaml") as f:
    config = yaml.safe_load(f)




def generate_pages():
    for page in config['pages']:
        template = env.get_template(page['name'])
        html = template.render(site=config['site'],page=page)
        with open(f"dist/{page['name']}","w") as  output:
            output.write(html)
        print(f"Writing Static {page['name']}")


generate_pages()