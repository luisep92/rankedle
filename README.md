## BOT RANKEDLE

### Requirements
- It's recommended to set the environment variable `$BOT_TOKEN` with the token of your Discord bot. **Either** you can replace it in the `docker run` command later.
```bash
export $BOT_TOKEN=<YOUR_TOKEN_HERE>
```
### Run in Docker
#### Requirements
- Docker

#### Build the container
Create docker image
```bash
docker build -t rankedle .
```
#### Run the container
Run the container and you are done. You can replace `$BOT_TOKEN` with your token if you don't want to set the environment variable.
```bash
docker run -e BOT_TOKEN=$BOT_TOKEN rankedle
```

### Run without container
#### Requirements
- Poetry
- FFMPEG

#### Installation
To install the dependencies simply run
```bash
poetry install
```

#### Running the bot
Just execute tue `bot.py` file
```bash
python3 ./src/rankedle/bot.py
```

### Usage
Before running the bot, don't forget to check the config file `config.yaml`.

When the bot is already running, a **mod** shall send the `!start` command in a **permitted channel**. Inmediately, the bot will prompt a message containing the `!help` command, and it will start to download and star guessing songs.
