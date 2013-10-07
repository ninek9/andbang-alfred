#!/usr/bin/python

import sys
import alp
import api
import teams

n = alp.Notification()
settings = alp.Settings()

param_str = sys.argv[1]
params = param_str.split(':')

if len(params) < 1:
    sys.exit()

command = params[0]

if len(params) == 2 and command == 'token':
    settings.set(token=params[1])
    teams.save()
    sys.exit()

if command == 'teams':
    teams.save()
    sys.exit()

if len(params) == 3:
    if command == 'ship':
        r = api.method('/tasks/' + params[2] + '/ship', params[1], {}, 'post').json()
        n.notify("Task was shipped", r["title"], r["id"])
    elif command == 'later':
        r = api.method('/tasks/' + params[2] + '/later', params[1], {}, 'post').json()
        n.notify("Task was latered", r["title"], r["id"])
    elif command == 'create':
        r = api.method('/me/tasks', params[1], {'title': params[2]}, 'post').json()
        n.notify("Task was created", r["title"], r["id"])