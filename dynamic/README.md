# Static Site Generation

```bash

# structure 
|- data
|   ---- config.yaml # configurations placeholders 
|- dist 
|   ---- assets 
|        ---- css
|        ---- images # static files
|        ---- js 
|   ---- downloads   # downloadable files organized 
|
|   ---- ezhil_tests # used as examples
|   ---- Ezhil-Publications # publication files
|   ---- *.html # generated html from templates
|- templates
|   ---- *.html # jinja templates 

# based on the configuration mentioned pages only considered for genration
```

## Builder

```bash 
python3 build.py # to build dist pages 
```

## pip dependencies

```bash
Jinja2
pyyaml 
```
