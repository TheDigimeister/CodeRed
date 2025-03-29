import praw
from textdistance import levenshtein

reddit = praw.Reddit(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    user_agent='BOT_DETECTOR/1.0'
)

def calculate_bot_score(username, k=100):
    user = reddit.redditor(username)
    submissions = list(user.new(limit=k))
    
    if not submissions:
        return 0, False

    scores = {
        'account_age': min((user.created_utc - 1136073600) / 1e8, 1),  # Normalized since 2006
        'karma_score': 1 - (user.link_karma + user.comment_karma) / 1e5,
        'content_similarity': sum(
            levenshtein.normalized_similarity(a.body, b.body)
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
    return bot_score, bot_score > 0.65

from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/check_user/<username>')
def check_user(username):
    score, is_bot = calculate_bot_score(username)
    return jsonify({
        'score': round(score, 2),
        'is_bot': is_bot,
        'metrics': {
            'account_age_days': (time.time() - user.created_utc)/86400,
            'total_karma': user.link_karma + user.comment_karma
        }
    })

