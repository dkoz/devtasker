# Dev Tracker App
 This is a simple development tracker based on [Patrickloeber](https://github.com/patrickloeber) todo python app.

## Features
 - Discord oauth with ID whitelist, allowing you to assign admins to the tracking workflow.
 - Add, delete and edit tasks on the list to keep track of progress.
 - All data stored locally.

## Setup
 Quick setup guide for the app.
 1. Create the python virtual environment.
 ```bash
 python3 -m venv venv
 source venv/bin/activate
 ```

 2. Install the dependencies.
 ```bash
 pip install -r requirements.txt
 ```

 3. Create your `.env` file.
 ```bash
 client_id='client id'
 client_secret='client secret'
 redirect_url='call back url'
 discord_id='your discord id'
 ```

 3. Run the environment.
 ```bash
 python main.py
  ```