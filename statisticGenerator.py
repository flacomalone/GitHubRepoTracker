import datetime
import pandas as pd
from config.allowedEvents import allowedEvents


def separatePerEventType(events_unsorted, eventType):
    consecutiveEvents = []
    for e in events_unsorted:
        if e["type"] == eventType:
            consecutiveEvents.append(e)
    return consecutiveEvents


def calculateMeanElapsedTime(consecutiveEventsList):
    if len(consecutiveEventsList) > 0:
        sum = 0
        for i in range(1, len(consecutiveEventsList)):
            first_date = datetime.datetime.strptime(consecutiveEventsList[i]["created_at"], '%Y-%m-%dT%H:%M:%SZ')
            second_date = datetime.datetime.strptime(consecutiveEventsList[i-1]["created_at"], '%Y-%m-%dT%H:%M:%SZ')
            sum += (second_date - first_date).total_seconds() / 3600
        return sum/len(consecutiveEventsList)
    else:
        return 0


def fetchEvents(repo):
    # This module determines which events are used for the statistics: occurred in the last 7 days range or the last 500
    # All types of events in a repo are considered for determining which are used for the statistics

    # Load events from that repo from disk (could be improved by using memory)
    events = pd.read_csv("data/fromGitHub/" + repo + '.csv').to_dict(orient='records')

    # get events occurred within the last week:
    current_date = datetime.date.today()
    past_week_date = current_date - datetime.timedelta(days=7)
    last_week_events = list(filter(lambda entry: past_week_date <= datetime.datetime.strptime(entry["created_at"], "%Y-%m-%dT%H:%M:%SZ").date() <= current_date, events))

    if len(last_week_events) < 500:
        return last_week_events
    else:
        return events[:500]


def calculateStatistics(repo_names):
    statistics = dict.fromkeys(repo_names)
    for repo in repo_names:
        time_elapsed_per_event_type = dict.fromkeys(allowedEvents)
        events_to_measure = fetchEvents(repo)
        for event_type in allowedEvents:
            consecutiveEvents = separatePerEventType(events_unsorted=events_to_measure, eventType=event_type)
            time_elapsed_per_event_type[event_type] = calculateMeanElapsedTime(consecutiveEvents)  # always expressed as hours
        statistics[repo] = time_elapsed_per_event_type

    # Save results for data persistence (overrides last records)
    df = pd.DataFrame(statistics)
    df.to_json("data/statistics.json", indent=2)

    print("Statistics Generator -> Statistics have now been created.")

    return statistics


if __name__ == "__main__":
    calculateStatistics()