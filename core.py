import praw
import os
import time
from dotenv import load_dotenv
from textdistance import levenshtein

load_dotenv()

username = os.getenv('YOUR_REDDIT_USERNAME')

reddit = praw.Reddit(
    client_id=os.getenv('YOUR_CLIENT_ID'),
    client_secret=os.getenv('YOUR_CLIENT_SECRET'),
    client_password=os.getenv('YOUR_REDDIT_PASSWORD'),
    username=username,
    user_agent="BOT_DETECTOR/1.0 (by u/" + username + ")",
)

def calculate_bot_score(user, k=100):
    submissions = list(user.submissions.new(limit=k))
    
    if not submissions:
        return 0, False

    scores = {
        'account_age': min((user.created_utc - 1136073600) / 1e8, 1),  # Normalized since 2006
        'karma_score': 1 - (user.link_karma + user.comment_karma) / 1e5,
        'content_similarity': sum(
            levenshtein.normalized_similarity(a.selftext, b.selftext)
            for a, b in zip(submissions, submissions[1:])
        ) / (len(submissions)-1) if len(submissions) > 1 else 0,
        'post_frequency': len(submissions) / (k * 24 * 3600)  # Posts per second
    }

    weights = {
        'account_age': 0.3,
        'karma_score': 0.25,
        'content_similarity': 0.3,
        'post_frequency': 0.15
    }

    bot_score = sum(scores[metric] * weights[metric] for metric in scores)
    print(scores)
    return bot_score, bot_score > 0.65

from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources=r'/check_user/*')

@app.route('/check_user/<username>')
def check_user(username):
    user = reddit.redditor(username)
    score, is_bot = calculate_bot_score(user)
    response = jsonify({
        'score': round(score, 2),
        'is_bot': is_bot,
        'metrics': {
            'account_age_days': (time.time() - user.created_utc)/86400,
            'total_karma': user.link_karma + user.comment_karma
        }
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
