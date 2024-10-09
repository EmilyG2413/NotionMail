"""
This is an internal integration tool for a Notion database which simulates
a messagig service. The tool is based off the Notion API and the unofficial
Notion SDK for python.

Owner: Emily Guo
Last Modified: 9/25/2024
Contact: yue.guo@utexas.edu

"""
#!python
from dotenv import load_dotenv
import os
from notion_client import Client
from datetime import datetime
import inquirer
from inquirer.errors import ValidationError

# Initialize Notion client
load_dotenv()
notion = Client(auth=os.getenv("NOTION_TOKEN"))

# Initialize Database to modify
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

def validate_non_empty(answers, current):
    """
    Ensure that the input is not an empty string.
    """
    if not current.strip():
        raise ValidationError("", reason="This field cannot be empty.")
    return True

def send_mail(sender, recipients, message):
    """
    This method is responsible for the sending a message to one
    or more recipiants.

    Args:
        sender (str): A string from user input for the name of the sender
        recipients (str): A comma-seperated string for the name(s) of the receiver(s)
        message (str): A String from user input for the message
    """

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Split recipients by comma and strip whitespace
    recipient_list = [recipient.strip() for recipient in recipients.split(',')]

    try:
        for recipient in recipient_list:
            # Create a row in the database
            new_page = notion.pages.create(
                parent={"database_id": DATABASE_ID},
                properties={
                    "Sender": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": sender
                                }
                            }
                        ]
                    },
                    "Recipient": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": recipient
                                }
                            }
                        ]
                    },
                    "Message": {
                        "title": [
                            {
                                "text": {
                                    "content": message
                                }
                            }
                        ]
                    },
                    "Sent Time": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": current_time
                                }
                            }
                        ]
                    }
                }
            )

            # Format and Print output
            print(f"\n╭─────────────────────────────────╮")
            print(f"   ✅ Message sent successfully!")
            print(f"╰─────────────────────────────────╯")
            print(f"From: {sender}")
            print(f"To: {recipient}")
            print(f"Message: {message}")
            print(f"Sent at: {current_time}")

    except Exception as e:
        print(f"⚠️  Error querying the database: {e}")

def read_mail(user):
    """
    This method is responsible for the reading all unread
    messages for one recipient. It will sort returned methods from most
    recently received to least recently received. The use may then specify
    if they "read" or "unread" the current message, if unread, the message
    will show up again the next time read for this recipient is called.

    Args:
        user (str): the recipient
    """
    try:
        response = notion.databases.query(
            **{
                "database_id": DATABASE_ID,
                "filter": {
                   "and": [
                        {
                            "property": "Recipient",
                            "rich_text": {
                                "equals": user
                            }
                        },
                        {
                            "property": "Read",
                            "checkbox": {
                                "equals": False  # Only fetch unread messages
                            }
                        }
                    ]
                },
                "sorts": [
                    {
                        "timestamp": "created_time",
                        "direction": "descending"  # Sort from most frequent to least
                    }
                ]
            }
        )

        if len(response["results"]) == 0:
            print(f"No messages for {user}.")
            return

        print(f"\n╭───────────────────────────╮")
        print(f"   ✉ Messages for {user}: ")
        print(f"╰───────────────────────────╯\n")

        for message in response["results"]:
            # Print Message
            sender = message["properties"]["Sender"]["rich_text"][0]["text"]["content"]
            content = message["properties"]["Message"]["title"][0]["text"]["content"]
            read_status = message["properties"]["Read"]["checkbox"]
            message_id = message["id"]
            print(f"From: {sender}")
            print(f"Message: {content}")
            print(f"Read: {'Yes' if read_status else 'No'}")
            mark_read = input("Mark as read? [y/n]: ").strip().lower()
            if mark_read == 'y':
                # Update the message to mark it as read
                notion.pages.update(
                    page_id=message_id,
                    properties={
                        "Read": {
                            "checkbox": True
                        }
                    }
                )
                print(f"Message from {sender} marked as read.")
            elif mark_read == 'n':
                # Update the message to mark it as unread
                notion.pages.update(
                    page_id=message_id,
                    properties={
                        "Read": {
                            "checkbox": False
                        }
                    }
                )
                print(f"Message from {sender} marked as unread.")
            print("───────────────────────────\n")

    except Exception as e:
        print(f"⚠️  Error querying the database: {e}")

def delete_mail(user):
    """
    This method is responsible for displaying all messages for a given
    user and allowing the user to select the one to delete.

    Args:
        user (str): the user (recipient) to delete messages for
    """
    response = notion.databases.query(
        database_id=DATABASE_ID,
        filter={
            "property": "Recipient",
            "rich_text": {
                "equals": user
            }
        },
    )

    if not response["results"]:
        print(f"No messages found for {user}.")
        return

    print(f"\n╭───────────────────────────╮")
    print(f"   ✉ Messages for {user}: ")
    print(f"╰───────────────────────────╯\n")
    # Display the messages with their IDs
    for index, message in enumerate(response["results"], start=1):
        sender = message["properties"]["Sender"]["rich_text"][0]["text"]["content"]
        content = message["properties"]["Message"]["title"][0]["text"]["content"]
        read_status = message["properties"]["Read"]["checkbox"]
        message_id = message["id"]

        print(f"ID: {index}")
        print(f"From: {sender}")
        print(f"Message: {content}")
        print(f"Read: {'Yes' if read_status else 'No'}")

        print("───────────────────────────\n")
    # Prompt the user to select a message to delete
    try:
        message_index = int(input("Enter the number of the message to delete: ")) - 1
        if message_index < 0 or message_index >= len(response["results"]):
            print("Invalid selection. Please try again.")
            return

        # Get the selected message ID
        selected_message = response["results"][message_index]
        selected_message_id = selected_message["id"]

        # Delete the message using the correct endpoint
        notion.pages.update(page_id=selected_message_id, archived=True)
        print(f"Message from {selected_message['properties']['Sender']['rich_text'][0]['text']['content']} deleted.")

    except ValueError:
        print("Please enter a valid number.")

def main():
    """
    Command prompt for mailing service, this prompt continues untl the user
    decides to exit.
    """
    print("\nWelcome to NotionMail!")

    while True:
        print(f"{'=' * 60}")
        options = [
            inquirer.List(
                'option',
                message="Please select an option",
                choices=['send', 'read', 'delete', 'exit']
            )
        ]
        # print("\nPlease select an option:")
        # print("- send: Send mail to a user.")
        # print("- read: Check a user's mail.")
        # print("- delete: Delete a message.")
        # print("- exit: Exit the application.\n")

        # option = input("Select an option: ").strip().lower()
        answers = inquirer.prompt(options)
        option = answers['option']

        if option == "send":
            questions=[
                inquirer.Text('sender', message="Sender", validate=validate_non_empty),
                inquirer.Text('recipient', message="Recipient", validate=validate_non_empty),
                inquirer.Text('message', message="Message", validate=validate_non_empty),
            ]
            answers = inquirer.prompt(questions)
            send_mail(answers['sender'], answers['recipient'], answers['message'])

        elif option == "read":
            questions=[
                inquirer.Text('user', message="User", validate=validate_non_empty)
            ]
            answers = inquirer.prompt(questions)
            read_mail(answers['user'])
        elif option == "delete":
            questions=[
                inquirer.Text('user', message="User", validate=validate_non_empty)
            ]
            answers = inquirer.prompt(questions)
            delete_mail(answers['user'])
        elif option == "exit":
            print("Exiting NotionMail. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
