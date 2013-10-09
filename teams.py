#!/usr/bin/python

import core
import feedback
import requests
import api
import notification
import settings

n = notification.Notification()
user_settings = settings.Settings()

def save():
    r = api.method('/me/teams')
    if r.status_code == 200:
        resp = r.json()
        if len(resp) > 0:
            user_settings.set(teams=resp)
            write_images()
            n.notify("AndBang Workflow Success", "Your teams were saved!", "Teams: " + ', '.join([team["name"] for team in resp]))
        else:
            n.notify("AndBang Workflow Error", "No teams were saved", "Please create one at http://andbang.com")
    else:
        n.notify("AndBang Workflow Error", resp["message"], "Visit http://andbang.com")

def write_images():
    teams = user_settings.get('teams', [])
    for team in teams:
        r = requests.get('http:' + team["thumbUrl"], stream=True)
        if r.status_code == 200:
            with open(core.storage('team-' + team['name']), 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)