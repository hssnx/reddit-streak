# Reddit Streak Bot

This GitHub Action automatically upvotes one new post from a set of subreddits twice per day.

## How to Use

### 1. Fork This Repository

Click the "Fork" button at the top-right of this page.

### 2. Create a Reddit App

Go to [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps) and click "create another app" at the bottom.

Fill the form as follows:

- **name**: `streak` (or anything)
- **type**: `script`
- **description**: _(optional) leave blank_
- **about url**: _(optional) leave blank_
- **redirect uri**: `http://localhost:8080`

Click "Create app" and save the following values:

- `client_id` (shown under the app name)
- `client_secret` (labelled as “secret”)

### 3. Generate Your Refresh Token

Run the `get_refresh_token.py` script provided in this repo.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 get_refresh_token.py
```

Enter your `client_id` and `client_secret` when prompted. Then, a browser window will open asking you to authorize. Once authorized, your **refresh token will be printed in the terminal**.

### 4. Add GitHub Secrets

In your forked repo:

- Go to **Settings → Actions secrets and variables → Actions → New repository secret**, and add the following secrets:

| Name                   | Value                                        |
| ---------------------- | -------------------------------------------- |
| `REDDIT_CLIENT_ID`     | your `client_id`                             |
| `REDDIT_CLIENT_SECRET` | your `client_secret`                         |
| `REDDIT_REFRESH_TOKEN` | your generated `refresh_token`               |
| `REDDIT_USER_AGENT`    | `script:streak-bot:v1.0 (by u/yourusername)` |

### 6. Enable and Test GitHub Actions

Go to the Actions tab in your repository and click on "Reddit Streak Bot". Click "Run workflow" to manually trigger it.

This allows you to verify everything is set up correctly. Once the workflow runs, check the logs to confirm the bot is working as expected.

If successful, the bot will continue running automatically twice per day at 09:00 and 21:00 UTC, upvoting a post from one of the specified subreddits.
