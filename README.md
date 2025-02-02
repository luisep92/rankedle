## BOT RANKEDLE

### Requirements
- You **must** provide a `.env` file at the root path of the project. This file must contain at least
```bash
BOT_TOKEN=YOUR_BOT_TOKEN
DJANGO_ADMIN=SUPERADMIN_USER
DJANGO_PASSWORD=SUPERADMIN_PASSWORD
```
### Run in Docker
#### Requirements
- Docker
- Docker-compose

#### Running the containers
Once you have prepared your `.env` file, simply run
```bash
docker-compose up
```
*Note that you will need admin rights to run this command.*

### For DEVs

### Run without container
#### Requirements
- Poetry
- FFMPEG

#### Dependencies
To install the dependencies simply run
```bash
poetry install
```

#### Introduction
The project contains two separate parts: the discord bot and the django web server.

The discord bot manages the callbacks and discord logic but abstracts an interface that manages how the maps/users/... are managed, so you can implement your own behavior on these.

The django webserver contains a SQLite database to manage the information about the maps, users, etc.


#### Discord bot

##### Running the bot
Just execute the `bot.py` file
```bash
python3 ./src/rankedle/bot.py
```

##### Usage
Before running the bot, don't forget to check the config file `config.yaml`.

When the bot is already running, a **mod** shall send the `!start` command in a **permitted channel**. Inmediately, the bot will prompt a message containing the `!help` command, and it will start to download and star guessing songs.


#### Django webserver
No database file is provided in the project so with the first run of django, a db.sqlite3 is going to be generated. 

Not to make things complicated, you can just run
```bash
cd src/web/
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

With the first migration, the database should have been generated, and the `initial_data.json` will be inserted in the database.

*Don't forget you will need a super user to manage the data in the admin panel*

##### Run the webserver
Once the initial steps are done, you can run the server
```bash
python manage.py runserver
```

Now you should be able to enter the admin panel through ***127.0.0.1:8000/admin***


#### Adding maps
A file named `songs_to_add.json` is provided. This file contains the data directly pulled from beatsaver.

In the admin panel, you should be able to go to the `Maps` section, and press `Add`.

This will lead you to the map insertion page. This page is automatically filled with the information of the next map from the `songs_to_add.json` file, which is not inserted in the database. Make sure that the information is correct, and add the permitted names if necessary, then just press add and the work should be done.
