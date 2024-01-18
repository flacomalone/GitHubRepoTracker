import json
import os.path
from flask import Flask, jsonify

app = Flask(__name__)
f = open("config/repositories.json")
repositories = json.load(f)
repo_names = [repo["name"] for repo in repositories]

@app.route('/repos', methods=['GET'])
def get_all_repos():
    if os.path.exists("data/statistics.json"):
        f = open("data/statistics.json")
        statistics = json.load(f)
        return jsonify(statistics)
    else:
        return jsonify({'error': 'Statistics are not yet available'}), 404


@app.route('/repo/<string:name>', methods=['GET'])
def get_repo_by_name(name):
    if os.path.exists("data/statistics.json"):
        f = open("data/statistics.json")
        statistics = json.load(f)
        if name not in repo_names:
            return jsonify({'error': 'That repository is not being monitored'}), 404
        else:
            return jsonify(statistics[name])
    else:
        return jsonify({'error': 'Statistics are not yet available'}), 404


def main():
    app.run(port=5000)
