# Generate API doc 

## Install packages

```bash
sudo pip3 install --upgrade 'pydoc-markdown>=4.0.0,<5.0.0' mkdocs
```

## Regenerate API documentation

```bash
pydoc-markdown -I AirzoneCloud -m AirzoneCloud -m Installation -m Group -m Device --render-toc > API.md
```

# Build new version and push to pypi

- update version in setup.py
- push new build on pypi

```bash
python setup.py sdist
twine upload --skip-existing dist/*
```
