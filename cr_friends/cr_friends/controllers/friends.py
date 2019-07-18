from cr_friends.config.mysqlconnection import connectToMySQL
from flask import render_template, request, redirect
from cr_friends.models.friend import Friend


friend = Friend()

class Friends:
    def index(self):
        result=friend.index()
        return render_template('index.html', friends=result)

    def create(self):
        friend.create()
        return redirect('/')