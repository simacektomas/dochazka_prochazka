from slack_bolt import App
from slack_bolt.context.ack.ack import Ack
from slack_bolt.context.say.say import Say
from slack_sdk.web.client import WebClient
import datetime
import json

from src import templates
import logging

#logging.basicConfig(level=logging.DEBUG)

tracked_trainings = {}
attendance = {}

app = App()

@app.command("/create_training")
def create_event(ack: Ack, say: Say, response, client: WebClient, command: dict):
    # Create message
    # Save the ID to the DB
    # Acknowledge data retrieval
    if command:
        ack()

    print(json.dumps(command, indent=2))
    if "text" not in command:
        client.chat_postEphemeral(
            channel=command["channel_id"],
            user=command["user_id"],
            text=f"You did not pass any parameters to command {command['command']}."
        )
        return

    args = command["text"].split()
    if len(args) != 2:
        client.chat_postEphemeral(
            channel=command["channel_id"],
            user=command["user_id"],
            text=f"Command {command['command']} requires date and place as parameters."
        )
        return

    res = client.chat_postMessage(
      channel=command["channel_id"],
      blocks=[templates.TRANING_MESSAGE]
    )
    if res["ok"]:
        tracked_trainings[res["ts"]] = res["message"]
    print(json.dumps(res.data, indent=2))

@app.event("reaction_added")
def reaction_add_handler():
    print(json.dumps([k for k in tracked_trainings], indent=2))
    print(json.dumps(attendance, indent=2))


@app.action("dropdown")
def training_dropdown_handler(body, client, respond, say, ack):
    # Acknowledge data retrieval to slack
    if body:
        ack()

    training = body["message"]["ts"]
    user = body["user"]["username"]

    #TODO: Save the user choice into the DB history
    #TODO: Update the training message with the username or remove the username

    print(json.dumps(body, indent=2))
    selected_options = body["actions"][0]["selected_option"]["value"]
    if selected_options == "confirm":
        if training not in attendance:
            attendance[training] = []
        if user not in attendance[training]:
            attendance[training].append(user)
    elif selected_options == "later":
      reaction = "eyes"
    else:
        if training not in attendance:
            attendance[training] = []
        if user in attendance[training]:
            attendance[training].remove(user)




def main():
    app.start(3000)


if __name__ == "__main__":
    main()
