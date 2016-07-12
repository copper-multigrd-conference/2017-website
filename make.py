#!/usr/local/bin/python

import os
import time
import yaml
import shutil
from jinja2 import Environment, FileSystemLoader

# make the live web directory if needed
# move old to a timestamp just in case
liveweb = './live'

if os.path.exists(liveweb):
    timestamp = time.strftime('%c').replace(' ', '-')
    shutil.move(liveweb, liveweb+'-'+timestamp)

os.makedirs(liveweb)

# parse, render each template here
env = Environment(loader=FileSystemLoader('./'))
files = ['_index.html']

# Load Data
with open("./data-common/student-paper-winners.yml", "r") as inf:
    student_paper_winners = yaml.load(inf)

with open("./data-common/previous-conferences.yml", "r") as inf:
    previous_conferences = yaml.load(inf)

with open("./data-conf/committee.yml", "r") as inf:
    committee = yaml.load(inf)

with open("./data-conf/deadlines.yml", "r") as inf:
    deadlines = yaml.load(inf)

for f in files:
    template_vars = {}
    if f == '_index.html':
        template_vars['name'] = 'index'  # for the nav bar
        template_vars['student_deadline'] = 'January'
        template_vars['abtract_deadline'] = 'January'
        template_vars['deadlines'] = deadlines

    html = env.get_template(f).render(template_vars)
    with open(os.path.join('./live/', f[1:]), 'w') as fout:
        fout.write(html)

# copy these directories as-is to the webdir
livedirs = ['font-awesome', 'bootstrap', 'css', 'images']
for d in livedirs:
    shutil.copytree(d, os.path.join(liveweb, d))
