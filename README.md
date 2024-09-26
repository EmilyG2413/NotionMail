# Notion Mail

**Owner:** Emily Guo \
**Last Modified:** 09/25/2024 \
**Contact:** [yue.guo@utexas.edu](mailto:yue.guo@utexas.edu) \

## Overview

This Notion Mail tool is a simple command-line interface or messaging service built on top of the Notion API and the unofficial Notion SDK for Python. It allows users to send, read, and delete messages, all of which are stored in a Notion database.

**Additional Improvements**: Read/unread messages, delete messages, timestamps of send, multiple receivers.

## Features

- **Send Mail:** Send a message from one user to one or multiple recipients.
- **Read Mail:** Retrieve unread messages for a specific user and mark them as read/unread.
- **Delete Mail:** Remove a message from the Notion database based on user input.

## Requirements

This tool requires the end user to have a notion integration and a database which the notion integration may access.

The database must contain the following columns in any order:
- **Sender**: text
- **Recipient**: text
- **Message**: title
- **Sent Time**: text
- **Read**: check box

The tool also requires the following installations:
- Python 3.7 or above
- The following Python packages:
  - `python-dotenv`
  - `notion-client`

The dependencies may be installed separately or with:

```bash
pip3 install -r requirements.txt
```

## Setup

1. **Clone or obtain the repository:**
   ```bash
   git clone https://github.com/EmilyG2413/NotionMail.git
   ```

2. **Create a `.env` file** in the project root, containing the following environment variables:

   ```bash
   NOTION_TOKEN=<integration-token>
   NOTION_DATABASE_ID=<database-id>
   ```

   - The `NOTION_TOKEN` is the Notion API integration token.
   - The `NOTION_DATABASE_ID` is the ID of the Notion database where messages will be stored, the ID is the first 32 characters after the notion.so/ before the ?.

3. **Run the application:**
   ```bash
   python notion_mail.py
   ```

## Error Handling

- If there are issues connecting to the Notion API or database, the app will display a relevant error message.
- Input validation is built into each prompt to guide the user through correct usage.

## Debugging

- If there are issues installing the `notion-client` installation, please ensure you are using a version of python3 as `pip` may be using python2 under certain setups.
- If there are issues are running the program, please ensure your .env is properly created and the database API is the first 32 characters of the web URL after the slash after notion.so.
- Should you have further issues, please contact Emily via email.

# Additional Information
# References
- [Notion Python SDK](https://github.com/ramnes/notion-sdk-py)
- [Notion Integration Demo](https://developers.notion.com/docs/create-a-notion-integration#give-your-integration-page-permissions)
- [Notion Working with Databases](https://developers.notion.com/docs/working-with-databases#adding-pages-to-a-database)
- [Notion Property Values](https://developers.notion.com/reference/property-value-object#title-property-values)
- Google Search
- Stack Overflow
- ChatGPT
- [Medium Articles](https://medium.com/@plasmak_/how-to-create-a-notion-page-using-python-9994bf01299)

# Future Improvements
- **Testing Suite**: For the future, I would like to write a comprehensive testing suite to standardize the testing procedure. Due to the time constraints, and my lack of familiarity with Python testing suites, I was not able to do more testing beyond using the tool. Thus should I have more time, the first thing I would like to implement is a testing suite.
- **Categories & Grouping**: As someone who likes to group their emails, I would also like to have some sort of categorization tool that allows me to group messages beyond read and unread.
- **Editing**: A sender may make typos and currently there is no way to remedy that, thus I want to add the ability for a user to edit any message they've sent.

# Design Decisions
- **Language**: My first decision was choosing which language to implement this tool in. My instinctive choice was Java which is the language I am the most familiar with, however on second thought I chose Python because I wanted more practice using Python since some of my classes use Python.
- **Code Organization**: Due to the intent of this being a small project, I chose to place all methods in a singular file. Moving forth, I would like to separate these features into their separate files so it is more organized.
- **Read**: For read, I initially gave back all messages that were read or unread as long as they belonged to the recipient. However, as I did some more testing, I noticed that it got annoying to keep giving back messages that I have already seen, which is what inspired me to have a read/unread message and modify read to only give back unread messages.