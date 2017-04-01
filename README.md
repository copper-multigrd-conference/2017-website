# website

Public website data

# To test:

1. clone: `git clone git@github.com:copper-multigrd-conference/website.git`
2. build: `./make.py`
3. view: the static html pages are built in `live`.  Use `python3 -m http.server 8000` and point your browser to `localhost:8000` to view.
4. sync: rsync the `live` directory to your favorite server

# Requirements

The data is stored with `yaml`.

The pages are generated with `jinja2`.

# Notes:

- bootstrap is v4 from branch `v4-dev`
- to retrieve program: `wget -r --level=0 -E --ignore-length -k -p -erobots=off -np -N -nH --cut-dirs=2 http://easychair.org/smart-program/Copper2017/index.html`
