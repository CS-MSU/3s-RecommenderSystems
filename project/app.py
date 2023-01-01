from flask import Flask, render_template, request, jsonify
from db_query import get_recommendations, get_user_info, get_watched


app = Flask(__name__)


@app.template_filter('formatdatetime')
def format_datetime(value, format="%d %b %Y"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        try:
            if request.form['contact'] == 'user_info':
                try:
                    data = get_user_info(request.form['uname'])
                    return render_template('user.html', data=data)
                except:
                    return jsonify({'Message': "No such user in database"}), 550
            elif request.form['contact'] == 'recommend':
                try:
                    recommend = get_recommendations(request.form['uname'])
                    return render_template('recommend.html', recommend=recommend)
                except:
                    return jsonify({'Message': "No such user in database"}), 550
            elif request.form['contact'] == 'watched':
                try:
                    movies = get_watched(request.form['uname'])
                    return render_template('watched.html', movies=movies)
                except:
                    return jsonify({'Message': "No such user in database"}), 550
        except:
            return jsonify({'Message': "Choose one options"}), 404
    return render_template('index.html')
