# NoSlackingOff
Automatic scrum management in Slack.
Features include:
1. Starting & ending projects
2. Setting custom sprint durations
3. Managing user stories
4. Managing tasks on the backlog (user assignments, time estimation)
5. NLP predictions for backlog items
6. Full-featured CLI with Slack slash commands
6. Burndowns

## CLI Commands
```
/project [start/end/show]
	start [-sprint/--sprintlength DAYS]

/userstory [add/remove]
	add NAME DESCRIPTION
	remove ID

/backlog [add/complete/remove/show]
	add NAME [-story/--userstory STORY] [-a/--assignee NAME] [-eta/--estimated_time HOURS]
	remove ID
	complete ID [-ata/--actual_time HOURS]
	modify ID PROPERTY VALUE

/burndown
```
