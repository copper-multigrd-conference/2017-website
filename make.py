from jinja2 import Environment, FileSystemLoader
import yaml

env = Environment(loader=FileSystemLoader('./'))

data = {'description': 'This is the index page.'}
html = env.get_template('_index.html').render(data)

with open('index.html', 'w') as f:
    f.write(html)

with open("./data-common/student-paper-winners.yml", "r") as inf:
    student_paper_winners = yaml.load(inf)

with open("./data-common/previous-conferences.yml", "r") as inf:
    previous_conferences = yaml.load(inf)

with open("./data-conf/committee.yml", "r") as inf:
    committee = yaml.load(inf)
