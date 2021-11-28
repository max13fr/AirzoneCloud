# Generate API doc 

## Prepare sphinx builder

```bash
sudo pip3 install sphinx sphinx-markdown-builder
```

```bash
sphinx-apidoc -o Sphinx-docs ./AirzoneCloud sphinx-apidoc --full -A 'max13fr'
```

```bash
echo "
import os
import sys
sys.path.insert(0,os.path.abspath('../'))
def skip(app, what, name, obj,would_skip, options):
    if name in ( '__init__',):
        return False
    return would_skip
def setup(app):
    app.connect('autodoc-skip-member', skip)
 " >> Sphinx-docs/conf.py
```

## Generate documentation

```bash
(cd Sphinx-docs && make markdown && cp _build/markdown/AirzoneCloud.md API.md)
```

## Source

https://stackoverflow.com/a/59128670

# Build new version

- update version in setup.py
- push new build on pypi

```bash
python setup.py sdist
twine upload dist/AirzoneCloud-X.X.X.tar.gz
```
