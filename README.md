# Pani z HR

## Requirements

- [Docker](https://www.docker.com)
- [Docker Compose](https://docs.docker.com/compose/)

## Environment Variables

| **Variable**              | **Required** | **Description**                                          |
|---------------------------|--------------|----------------------------------------------------------|
| `DISCORD_BOT_TOKEN`       | Yes          | The Discord application secret                           |
| `DISCORD_GUILD_ID`        | Yes          | The ID of your guild                                     |
| `RECRUITMENT_CATEGORY_ID` | Yes          | The ID of your recruitment channels category             |
| `OFFICER_ROLE_ID`         | Yes          | The ID of the Officer role                               |
| `CHANNEL_ACCEPTED_ID`     | Yes          | The ID of the accepted application channel               |
| `CHANNEL_REJECTED_ID`     | Yes          | The ID of the rejected application channel               |
| `CHANNEL_NO_CONTACT_ID`   | Yes          | The ID of the application channel when there is no reply |

## Usage

### Building the image

```
docker compose build
```

### Running the bot

```
docker compose up
```

### Formatting the code

```
docker compose run bot fmt
```

### Linting the code

```
docker compose run bot lint
```
