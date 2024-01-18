import os

import pandas as pd
import requests
from config.github_token import github_token as token
import json

etags_saved = False


def getEventsFromRepo(repo, e_tags_dict):
    headers = {'Authorization': 'token ' + token, 'If-None-Match': e_tags_dict[repo["name"]]}
    url = f'https://api.github.com/repos/{repo["owner"]}/{repo["name"]}/events'
    response = requests.get(url, headers=headers, params={'per_page': 100})

    if e_tags_dict[repo["name"]] is None:
        e_tags_dict[repo["name"]] = response.headers['ETag']

    if response.status_code == 304:  # No new events since last poll
        print("Event Retriever -> No new GitHub events from repo: " + repo["name"])
        return -1
    elif response.status_code != 200:  # Raise an error if there is an error
        raise Exception(f'Error retrieving events: {response.status_code}')
    else:
        data = response.json()

        # Just keep event type and date to avoid storing unnecessary information that can lead to formatting errors
        events = []
        for e in data:
            events.append({"type": e["type"], "created_at": e["created_at"]})
        return events


def queryGitHub(repositories, e_tags_dict):
    for repo in repositories:
        result = getEventsFromRepo(repo, e_tags_dict)
        if result != -1:
            # Save results for data persistence
            saveResultsToDisk(result, repo["name"])
    if not etags_saved:
        saveETags(e_tags_dict)


def saveResultsToDisk(result, repo_name):
    if os.path.exists("data/fromGitHub/" + repo_name + '.csv'):
        # Load data from disk
        old_values = pd.read_csv("data/fromGitHub/" + repo_name + '.csv').to_dict(orient='records')

        # Identify which new entries to add to the system
        for e in result:
            if e not in old_values:
                old_values.insert(0, e)  # Descending order
        df = pd.DataFrame(old_values)
    else:
        # save all of them
        df = pd.DataFrame(result)

    # save
    df.to_csv("data/fromGitHub/" + repo_name + ".csv", index=False)


def saveETags(e_tags_dict):
    # save them to disk to not ask for them again after reboot
    print("Event Retriever -> Saving new ETags")
    with open("config/etags.json", 'w') as f:
        json.dump(e_tags_dict, f, indent=2)
    global etags_saved
    etags_saved = True


def prepareETags(repo_names):
    # ETag are used for efficient polling in case there are no modifications in the repo
    # More info in https://docs.github.com/en/rest/activity/events?apiVersion=2022-11-28#about-github-events
    etag_config_file_path = "config/etags.json"
    if os.path.exists(etag_config_file_path):
        with open(etag_config_file_path, 'r', encoding='utf-8') as f:
            e_tags_dict = json.load(f)
            if set(e_tags_dict.keys()) != set(repo_names):  # out-of-date etags (new repos)
                e_tags_dict = dict.fromkeys(repo_names)
    else:
        e_tags_dict = dict.fromkeys(repo_names)  # Start with None values
    return e_tags_dict