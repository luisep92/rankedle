## BOT RANKEDLE

### Requirements
- Docker
- It's recommended to set the environment variable `$BOT_TOKEN` with the token of your Discord bot. **Either** you can replace it in the `docker run` command later.
```bash
export $BOT_TOKEN=<YOUR_TOKEN_HERE>
```

### Build the container
```bash
docker build -t rankedle .
```
### Run the container
Run the container and you are done. You can replace `$BOT_TOKEN` with your token if you don't want to set the environment variable.
```bash
docker run -e BOT_TOKEN=$BOT_TOKEN rankedle
```