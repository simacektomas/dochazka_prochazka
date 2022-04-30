from slack_bolt import App
import logging

app = App()


@app.command("/create_event")
def create_event(ack, body, say):
    # Create message
    # Save the ID to the DB
    pass


@app.event("reaction_added")
def reaction_handler(body, say):
    # Check if the reaction was added to the tracked message
    # If yes save it to the DB, possibly update frontend statistics ....
    pass


def main():
    app.start(3000)


if __name__ == "__main__":
    main()
