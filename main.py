import json
import os.path
import threading
import time

from eventRetreiver import prepareETags, queryGitHub
from statisticGenerator import calculateStatistics
from server import main as API_main

f = open("config/repositories.json")
repositories = json.load(f)

# Check that there are no more than 5 repos to monitor
if len(repositories) > 5:
    raise Exception("The maximum number of repositories is 5.")

repo_names = [repo["name"] for repo in repositories]

if os.path.exists("data/statistics.json"):
    f = open("data/statistics.json")
    statistics = json.load(f)
else:
    statistics = None

# Launch API server as a thread
thread = threading.Thread(target=API_main)
thread.daemon = True
thread.start()

query_interval = 30  # seconds
e_tags_dict = prepareETags(repo_names)
while True:
    queryGitHub(repositories, e_tags_dict)
    calculateStatistics(repo_names)
    time.sleep(query_interval)