from app import app, cursor
from flask import request
import json

@app.route("/db/api/clear/", methods = ['POST'])
def clear():
    cursor.execute("DELETE FROM Subscription")
    cursor.execute("DELETE FROM Post")
    cursor.execute("DELETE FROM Thread")
    cursor.execute("DELETE FROM Forum")
    cursor.execute("DELETE FROM Forum_User")
    cursor.execute("DELETE FROM Follower")
    cursor.execute("DELETE FROM User")
    response = json.dumps({"code": 0, "response": "OK"})
    return response

@app.route("/db/api/status/", methods = ['GET'])
def status():
    db_info = { "forum": 0, "user": 0, "thread": 0, "post": 0 }
    cursor.execute("SELECT COUNT(*) FROM Forum")
    db_info["forum"] = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM User ")
    db_info["user"] = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Thread")
    db_info["thread"] = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Post")
    db_info["post"] = cursor.fetchone()[0]
    response = json.dumps({"code": 0, "response": db_info})
    return response