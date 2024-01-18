# GitHub Repo Tracker

Author: David Tena Gago

## Project objective
This application tracks activities on GitHub using the GitHub Events API. It monitors up to five configurable repositories and generates statistics based on a rolling window of either 7 days or 500 events, whichever is less. These statistics are made available to end clients via a REST API.

**NOTE: the statistics are measured in hours**

The application consists of three main components:
- **Event Retriever**: This component retrieves events from the configured repositories using the GitHub Events API.
- **Statistic Generator**: This component generates statistics based on the queried events. It calculates the average time between consecutive events for each combination of event type and repository name.
- **API Server**: This component exposes a REST API for retrieving statistics on a separate thread. It provides endpoints for each combination of event type and repository name, returning the average time between consecutive events.

### Characteristics
- The application runs continuously, collecting events from the configured repositories given a configurable frequency in seconds. The data is stored in ``data/fromGitHub``. The only data that is saved is the event type and the date when it occurred in order to save space in disk.
- The application can connect to the Internet and make requests to the GitHub API, and the user has a valid GitHub token that must be specified in ``/config/github_token.py``.
- The maximum number of repositories to monitor is 5.
- The project will yield statistics of events occurred within the last 90 days, in compliance with GitHub's Event API policy.
- The repositories are configurable, and defined in ``/config/repositories.json``.
- The event types considered to be queried are defined in ``/config/events.json`` and by default are all the events present in GitHub's official documentation:
  - CommitCommentEvent
  - CreateEvent
  - DeleteEvent
  - ForkEvent
  - GollumEvent
  - IssueCommentEvent
  - IssuesEvent
  - MemberEvent
  - PublicEvent
  - PullRequestEvent
  - PullRequestReviewEvent
  - PullRequestCommentEvent
  - PullRequestReviewThreadEvent
  - PushEvent
  - ReleaseEvent
  - SponsorShipEvent
  - WatchEvent
- The application retains data through application restarts by persisting data to disk.
- The app is developed to calculate the statistics at a given frequency instead of calculating them upon a request to maximize scalability and performance
- The app makes use of etags, which allow optimising API querying when there are no changes in the responses. Thus, the requests are not counted in GitHub's server, facilitating bandwidth and API use rate. These etags are calculated the first time upon a new configuration of repositories, and are stored in ``config/etags.json``.
- It is assumed that the user will specify correctly the information related to the repos to be monitored, as well as provision of the necessary token for the API.

## Usage

to run the app, simply run ``main.py``

on the client side, in order to see the reported stats, you can do a GET request:
```http request
### To get the stats of a single repo
GET http://localhost:80/repo/<repo to query>
Accept: application/json

### to get the stats of all the repos monitored
GET http://localhost:5000/repos
Accept: application/json
```

The output for all the repos should look like:
```json
{
  "Resemblyzer":{
    "CommitCommentEvent":0.0,
    "CreateEvent":0.0,
    "DeleteEvent":0.0,
    "ForkEvent":0.0,
    "GollumEvent":0.0,
    "IssueCommentEvent":0.0,
    "IssuesEvent":0.0,
    "MemberEvent":0.0,
    "PublicEvent":0.0,
    "PullRequestEvent":0.0,
    "PullRequestReviewEvent":0.0,
    "PullRequestCommentEvent":0.0,
    "PullRequestReviewThreadEvent":0.0,
    "PushEvent":0.0,
    "ReleaseEvent":0.0,
    "SponsorShipEvent":0.0,
    "WatchEvent":14.403
  },
  "openpilot":{
    "CommitCommentEvent":0.0,
    "CreateEvent":1.2548611111,
    "DeleteEvent":0.4235185185,
    "ForkEvent":1.4620833333,
    "GollumEvent":0.0,
    "IssueCommentEvent":0.5085606061,
    "IssuesEvent":0.0,
    "MemberEvent":0.0,
    "PublicEvent":0.0,
    "PullRequestEvent":0.68375,
    "PullRequestReviewEvent":0.0,
    "PullRequestCommentEvent":0.0,
    "PullRequestReviewThreadEvent":0.0,
    "PushEvent":0.3771825397,
    "ReleaseEvent":0.0,
    "SponsorShipEvent":0.0,
    "WatchEvent":0.4989666667
  },
  "onnx":{
    "CommitCommentEvent":0.0,
    "CreateEvent":0.0,
    "DeleteEvent":0.0,
    "ForkEvent":8.6649074074,
    "GollumEvent":0.0,
    "IssueCommentEvent":3.6691025641,
    "IssuesEvent":7.7880092593,
    "MemberEvent":0.0,
    "PublicEvent":0.0,
    "PullRequestEvent":0.4058333333,
    "PullRequestReviewEvent":4.2240798611,
    "PullRequestCommentEvent":0.0,
    "PullRequestReviewThreadEvent":0.0,
    "PushEvent":0.0,
    "ReleaseEvent":0.0,
    "SponsorShipEvent":0.0,
    "WatchEvent":1.5379761905
  },
  "tensorflow":{
    "CommitCommentEvent":0.0,
    "CreateEvent":0.0,
    "DeleteEvent":0.0,
    "ForkEvent":1.6387301587,
    "GollumEvent":0.0,
    "IssueCommentEvent":0.3298498498,
    "IssuesEvent":0.8716468254,
    "MemberEvent":0.0,
    "PublicEvent":0.0,
    "PullRequestEvent":3.57,
    "PullRequestReviewEvent":0.0,
    "PullRequestCommentEvent":0.0,
    "PullRequestReviewThreadEvent":0.0,
    "PushEvent":0.5283472222,
    "ReleaseEvent":0.0,
    "SponsorShipEvent":0.0,
    "WatchEvent":0.5867690058
  },
  "crewAI":{
    "CommitCommentEvent":0.0,
    "CreateEvent":0.0,
    "DeleteEvent":0.0,
    "ForkEvent":0.973,
    "GollumEvent":0.0,
    "IssueCommentEvent":1.0369444444,
    "IssuesEvent":1.9838888889,
    "MemberEvent":0.0,
    "PublicEvent":0.0,
    "PullRequestEvent":2.2927777778,
    "PullRequestReviewEvent":0.0,
    "PullRequestCommentEvent":0.0,
    "PullRequestReviewThreadEvent":0.0,
    "PushEvent":0.0109722222,
    "ReleaseEvent":0.0,
    "SponsorShipEvent":0.0,
    "WatchEvent":0.1447372372
  }
}
```