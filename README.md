# LINE Bot - Leetcode question picker

The bot randomly picks Leetcode questions for you.

## Usage

After deploying the application and configuring the LINE official account webhook settings, your official account should
be ready to serve with following commands.

| Command | Description               |
|---------|:--------------------------|
| `選題`    | Pick three easy questions |

## Deployment

1. Build a Docker image.

    ```bash
    docker image build --platform amd64 -t leetcode-picker:latest .
    ```    

2. Find a place to host the application.
3. Configure environment variables.

| env                   |
|:----------------------|
| `LINE_CHANNEL_TOKEN`  |
| `LINE_CHANNEL_SECRET` |
