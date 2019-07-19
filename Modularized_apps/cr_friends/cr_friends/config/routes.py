from cr_friends import app
from cr_friends.controllers.friends import Friends

friends=Friends()

@app.route('/')
def index():
    return friends.index()

@app.route('/create_friend', methods=['POST'])
def create():
    return friends.create()