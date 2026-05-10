# Rankedle

A Discord "guess the song" game using [BeatSaver](https://beatsaver.com) content. **The Día de los Inocentes prank shipped — the over-engineered rewrite did not.** This README tells both, because the second story is the lesson.

---

## Two versions, only one of which made it

**December 28th 2024 — the prank that worked.** A small Discord bot that picked random Beat Saber songs and ran a "guess the title" loop. Maps and answers came from JSON files. No database, no admin panel, no containers. It ran for the day, did its job, and turned off — which is what was asked of it.

**January 2025 — the implementation that didn't.** A few weeks later someone in the community asked if it could become a persistent thing — admin panel, scoring, user history, deployable. I said yes and started this Django + Docker rewrite, which is what's in this repo. SQLite + ORM models, a Django admin for managing maps and permitted-name aliases, Poetry, multi-container Docker Compose, REST API. It works. It never got deployed.

**What's actually in production today.** A colleague added Beat Saber title guessing to their own community bot using simple **string-distance matching** — no Django, no container, no admin panel. Slightly worse matching results than this version would have produced. Has been running continuously for over a year.

---

## What is Rankedle (the Django version)

A Discord bot + Django backend designed to run a "guess the song" game on top of BeatSaver content. The bot handles the interactive flow; Django provides storage, an admin panel for managing maps and permitted-name aliases, and (later) a REST API.

Architecture:

- A Discord bot handling real-time commands and game state (`src/rankedle/`)
- A Django backend with SQLite and ORM models (`src/web/`)
- A clean interface between "game logic" and "data management" — the bot talks to the backend through a thin layer; the backend can be replaced without touching Discord
- Automated deployment using Docker and Poetry

---

## Lesson learned

Avoid overengineering when a simpler solution solves the real problem.

The clearest evidence in this repo is `src/web/SongManager/admin.py`: **five factory functions that return a class** — `BaseMapDifficultyFormSetWithParams`, `BasePermittedNameFormsetWithParams`, `MapDifficultyInLineWithParam`, `PermittedNameInlineWithParam`, `MapAdminFormWithParam`. Same shape every time. Django's admin classes are declarative and don't natively accept runtime parameters, but I needed runtime data (the next map from `songs_to_add.json`) to seed initial values in the form, so the workaround is to wrap each admin class in a factory function that closes over the data and returns the class with the params baked in. It works. It is also the kind of thing you write when the requirement could have been satisfied with much less.

The colleague's string-distance bot does what users actually wanted: tell them whether they got a song name right with reasonable tolerance. That is the entire requirement. Everything past that — admin panels, ORM, REST API, Docker — was me building a product nobody asked to maintain.

Real users preferred a simpler system that worked consistently to a perfect one that needed maintenance.

---

## Requirements

You **must** provide a `.env` file at the project root containing at least:

```bash
BOT_TOKEN=YOUR_BOT_TOKEN
DJANGO_ADMIN=SUPERADMIN_USER
DJANGO_PASSWORD=SUPERADMIN_PASSWORD
```

## Run in Docker

Needs Docker and Docker Compose. Once your `.env` file is in place:

```bash
docker-compose up
```

*Admin rights needed for this command.*

## Run without container (for devs)

Needs Poetry and FFMPEG.

```bash
poetry install
```

The project contains two parts: the Discord bot and the Django webserver. The bot manages callbacks and Discord logic but abstracts an interface for how maps/users/etc. are managed, so you can implement your own behaviour on these. The webserver holds a SQLite database for the information about maps, users, scores.

### Discord bot

```bash
python3 ./src/rankedle/bot.py
```

Before running, check the config file `src/rankedle/config.yaml`. Once running, a **mod** sends `!start` in a permitted channel — the bot prints `!help` and starts downloading and guessing songs.

### Django webserver

No database file is provided, so the first run generates `db.sqlite3` and seeds it from `initial_data.json`.

```bash
cd src/web/
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The admin panel is at `127.0.0.1:8000/admin`. You'll need that superuser to manage data there.

### Adding maps

`src/web/SongManager/songs_to_add.json` contains data pulled directly from BeatSaver. In the admin panel, go to `Maps → Add` — the page is auto-filled with the next map from the JSON queue (this is what the factory-function admin classes are for). Verify the information, add permitted-name aliases if needed, and save.
