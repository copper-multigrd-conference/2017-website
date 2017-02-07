import csv
import pandas as pd
import re

# ### Process
#
# 1. load `csv` layout file
# 2. Parse algorithm:
#     - If DayOfWeek and "Sesson" are included in title:
#         - log DayOfWeek
#         - log session ID: 1, 2, 3 or 1a, 2b, 3a etc
#         - log submisssion id
# 3. load `csv` latest submissions file
#
#
# Assuptions:
#     - Session 1: 800 - 1005
#     - Session 2: 1025 - 1230
#     - Session 3: 1630 - 1835
#     - Continental breakfast before session 1
#     - Coffee break after session 1
#     - Lunch after session 2
#     - Coffee break before session 3
#     - Dinner after session 3 (if no banquet)
#
# Evening Events:
#     - Banquet: define time
#     - tutorials: define time


def generate(layoutfile='./data-not-in-version-control/Copper 2017_data - Submissions.csv',
             latestdatafile='./data-not-in-version-control/Copper 2017_data_2017-02-06.xlsx'):

    data = pd.read_csv(layoutfile, encoding='latin1')

    program = {}
    daysofweek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday']
    gettitle = False

    for idx, row in data.iterrows():
        if 'END OF CONFERENCE' in row['title']:
            break

        day = [d for d in daysofweek if d+' Session' in row['title']]
        if day:
            # session row
            currentday, _, sessionnumfull = row['title'].split()
            print('\n', currentday, sessionnumfull)

            # parallel id
            parallel = 0
            if sessionnumfull[-1] == 'b':
                parallel = 1
            sessionnum = int(sessionnumfull[0])-1

            # initialize
            if currentday not in program:
                # three sessions
                program[currentday] = [[], [], []]

            # five speaker slots for each parallel session
            program[currentday][sessionnum] += [{'title': None,
                                                 'talks': [0, 0, 0, 0, 0]}]
            gettitle = True
            continue

        if gettitle:
            # row after session is the title
            print(row['title'])
            title = row['title'].strip()
            program[currentday][sessionnum][parallel]['title'] = title
            gettitle = False
            talknum = 0
            continue

        # next rows until session are submissions
        submissionnum = int(row["#"])
        program[currentday][sessionnum][parallel]['talks'][talknum] = submissionnum
        talknum += 1

    # remove last session
    program['Thursday'] = program['Thursday'][:2]

    # check data
    total = 0
    for key in program:
        for s in program[key]:
            for p in s:
                for t in p['talks']:
                    if t > 0:
                        total += 1
    print("%d talks" % total)

    xls = pd.ExcelFile(latestdatafile)

    latestdata = xls.parse('Submissions')
    latestdata = latestdata.set_index("#")

    authordata = xls.parse('Authors')

    for key in program:
        for s in program[key]:
            for p in s:
                p['titles'] = ['' for i in range(5)]
                p['abstract'] = ['' for i in range(5)]
                p['authors'] = ['' for i in range(5)]
                p['keywords'] = ['' for i in range(5)]
                p['speaker'] = [None for i in range(5)]
                p['webpages'] = ['' for i in range(5)]
                for i, t in enumerate(p['talks']):
                    if t > 0:
                        p['titles'][i] = latestdata.loc[t]['title']
                        abstract = latestdata.loc[t]['abstract']
                        abstract = re.sub('(?<!\n)\n(?!\n)', ' ', abstract)  # replace single \n
                        abstract = abstract.replace('\n', '<br/>')  # replace \n with <br/>
                        abstract = re.sub('\s\s+', ' ', abstract)  # remove multiple spaces
                        p['abstract'][i] = abstract
                        p['keywords'][i] = latestdata.loc[t]['keywords'].split()

                        df = authordata[authordata['submission #'] == t]
                        df = df.fillna('')
                        authors = [f+' '+l for f, l in zip(df['first name'], df['last name'])]
                        speaker = [i for i, b in enumerate(df['speaker?'].tolist()) if b.encode() == b'\xe2\x9c\x94']
                        if len(speaker) > 0:
                            speaker = speaker[0]
                        else:
                            speaker = 0
                        p['authors'][i] = authors
                        if 'oliver' in authors:
                            print(authors)
                        p['speaker'][i] = speaker
                        p['webpages'][i] = list(df['Web page'].values)

    return program
