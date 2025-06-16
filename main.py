import os
import random
import praw

# Load credentials from environment variables (GitHub Actions secrets or .env file)
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    refresh_token=os.getenv("REDDIT_REFRESH_TOKEN"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def upvote_one_post(subreddits):
    subreddit_name = random.choice(subreddits)
    subreddit = reddit.subreddit(subreddit_name)

    for post in subreddit.new(limit=10):
        if not post.likes:
            post.upvote()
            print("Upvoted:", post.title)
            print("Post URL:", f"https://www.reddit.com{post.permalink}")
            print("Subreddit:", f"r/{subreddit_name}")
            return

if __name__ == "__main__":
    subreddits = [
        "agi",
        "askphilosophy",
        "homelab",
        "dataisbeautiful",
        "singularity",
        "SideProject",
        ## Add more subreddits here if you want
    ]
    upvote_one_post(subreddits)
