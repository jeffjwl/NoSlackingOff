@app.event("app_home_opened")
def update_home_tab(client, event, logger):
  try:
    # views.publish is the method that your app uses to push a view to the Home tab
    client.views_publish(
      # the user that opened your app's app home
      user_id=event["user"],
      # the view object that appears in the app home
      view={
        "type": "home",
        "callback_id": "home_view",

        # body of the view
        "blocks": [
		{
			"type": "divider"
		},
		{
			"type": "divider"
		},
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Create a new task",
				"emoji": true
			}
		},
		{
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"multiline": true,
				"action_id": "plain_text_input-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Task Description",
				"emoji": true
			}
		},
		{
			"type": "input",
			"element": {
				"type": "multi_users_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select users",
					"emoji": true
				},
				"action_id": "multi_users_select-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Select Users",
				"emoji": true
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Pick a date for the deadline."
			},
			"accessory": {
				"type": "datepicker",
				"initial_date": "1990-04-28",
				"placeholder": {
					"type": "plain_text",
					"text": "Select a date",
					"emoji": true
				},
				"action_id": "datepicker-action"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Submit Task",
						"emoji": true
					},
					"value": "click_me_123",
					"action_id": "actionId-0"
				}
			]
		},
		{
			"type": "divider"
		}
	]
      }
    )
  
  except Exception as e:
    logger.error(f"Error publishing home tab: {e}")