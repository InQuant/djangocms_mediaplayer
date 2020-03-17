# Media Player Plugin (DjangoCMS)   

> A simple but effective and highly customizable media player for DjangoCMS 

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

Customize your HTML media player easily through overriding the css styles or create custom Templates for your Player.

### Dependencies
- django
- django-cms
- django-sekizai
- django-filer



- Use <a href="http://recordit.co/" target="_blank">**Recordit**</a> to create quicks screencasts of your desktop and export them as `GIF`s.
- For terminal sessions, there's <a href="https://github.com/chjj/ttystudio" target="_blank">**ttystudio**</a> which also supports exporting `GIF`s.

**Demo**

![Recordit GIF](https://thumbs.gfycat.com/ClearcutKindBactrian-size_restricted.gif)


---

## Installation

- Install from PyPI (or you [manually download from PyPI]()):
```shell script
pip install djangocms_mediaplayer
```

- Add `djangocms_mediaplayer` to you INSTALLED_APPS in django's `settings.py`
```python
INSTALLED_APPS = (
    # other apps
    "djangocms_mediaplayer",
)
```

- Run `migrate`
```shell script
python manage.py migrate
```

## License

[MIT](LICENSE)