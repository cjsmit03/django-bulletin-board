import requests


def get_reddit_posts(subreddit):
    """
    Fetch the latest posts from a subreddit.
    Returns a list of posts.
    """

    url = f"https://www.reddit.com/r/{subreddit}/.json"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    print("Status Code:", response.status_code)

    if response.status_code != 200:
        return [{
            "title": f"Reddit returned HTTP {response.status_code}",
            "author": "System",
            "url": "https://www.reddit.com/wiki/api/"
        }]

    data = response.json()

    posts = []

    for post in data["data"]["children"]:
        posts.append({
            "title": post["data"]["title"],
            "author": post["data"]["author"],
            "url": "https://reddit.com" + post["data"]["permalink"],
        })

    return posts
