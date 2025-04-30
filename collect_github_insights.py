from __future__ import print_function, division, absolute_import

import sys
import pprint
try:
    from agithub.GitHub import GitHub
except ImportError as e:
    print("Please first install 'agithub' package by calling `pip install arestclient`")
    sys.exit(1)

# Target Github repository
owner, repo = 'vertica', 'vertica-python'

# Create a GitHub object using an access token
g = GitHub(token='ADD YOUR GITHUB ACCESS TOKEN HERE!')

# Get the total number of watchers, stargazers and forks
status, repoinfo = g.repos[owner][repo].get()
forks_count = repoinfo['forks_count']
stargazers_count = repoinfo['stargazers_count']
watchers_count = repoinfo['subscribers_count']
print(f'\n\nwatch:{watchers_count}  star:{stargazers_count}  fork:{forks_count}')

# Get the total number of views and breakdown per day for the last 14 days
status, views = g.repos[owner][repo].traffic.views.get()
print("\n\n==> Views")
pprint.pprint(views)

# Get the total number of clones and breakdown per day for the last 14 days
status, clones = g.repos[owner][repo].traffic.clones.get()
print("\n\n==> Clones")
pprint.pprint(clones)
