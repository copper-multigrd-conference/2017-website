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
files = ['_index.html', '_people.html', '_student.html', '_about.html',
         '_lodging.html']


def prune_blank(somelist, key):
    somelist = [c for c in somelist if c[key] is not None]
    return somelist

# Load Data
with open("./data/info.yml", "r") as inf:
    info = yaml.load(inf)

with open("./data/student-paper-winners.yml", "r") as inf:
    student_paper_winners = yaml.load(inf)

with open("./data/previous-conferences.yml", "r") as inf:
    previous_conferences = yaml.load(inf)
    previous_conferences = prune_blank(previous_conferences, 'year')
    # now order by years
    previous_conferences = sorted(previous_conferences,
                                  key=lambda k: k['year'],
                                  reverse=True)

with open("./data/committee.yml", "r") as inf:
    committee = yaml.load(inf)
    committee = prune_blank(committee, 'name')
    # order by last part of last name
    committee = sorted(committee, key=lambda k: k['name'].split()[-1])

with open("./data/deadlines.yml", "r") as inf:
    deadlines = yaml.load(inf)

for f in files:
    template_vars = {}
    template_vars['info'] = info
    template_vars['deadlines'] = deadlines
    template_vars['previous_conferences'] = previous_conferences
    template_vars['committee'] = committee
    template_vars['student_paper_winners'] = student_paper_winners

    html = env.get_template(f).render(template_vars)
    with open(os.path.join('./live/', f[1:]), 'w') as fout:
        fout.write(html)

# copy these directories as-is to the webdir
livedirs = ['font-awesome', 'bootstrap', 'css', 'images']
for d in livedirs:
    shutil.copytree(d, os.path.join(liveweb, d))
