# -*- coding: utf-8 -*-
from app import app, cursor
from functions import *
from User import *
from Forum import *
from flask import request
import Post
import json

@app.route("/db/api/thread/create/", methods = ['POST'])
def createThread():
    logging.info("================Thread CREATION")
    try:
        forum = request.json["forum"]
        title = request.json["title"]
        isClosed = request.json["isClosed"]
        date = request.json["date"]
        message = request.json["message"]
        slug = request.json["slug"]
        user  = request.json["user"]
    except:
        return json.dumps({"code": 2, "response": error_messages[2]})

    try:
        isDeleted = request.json["isDeleted"]
    except:
        isDeleted = False

    try:
        id_Forum = getForumDetailsByShortName(forum)["id"]
        id_User = getUserInfoByEmail(user)["id"]
    except:
        return json.dumps({"code": 2, "response": error_messages[2]})

    sql = "INSERT INTO Thread(title, message, slug, date, isClosed, isDeleted, idForum, idAuthor, likes, dislikes) " \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql,      [title, message, slug, date, isClosed, isDeleted, id_Forum, id_User, 0    , 0])

    sql = "SELECT MAX(idThread) FROM Thread"
    cursor.execute(sql)
    idTh = cursor.fetchone()[0]

    answer = {}
    answer["date"] = date
    answer["forum"] = forum
    answer["id"] = idTh
    answer["isClosed"] = isClosed
    answer["isDeleted"] = isDeleted
    answer["likes"] = 0
    answer["dislikes"] = 0
    answer["message"] = message
    answer["points"] = answer["likes"] - answer["dislikes"]
    answer["posts"] = 0
    answer["slug"] = slug
    answer["title"] = title
    answer["user"] = user
    response = json.dumps({"code": 0, "response": answer })
    logging.info("  Answer : " + response)
    logging.info("================SUCCESSFUL THREAD CREATION\n")
    return response
    
@app.route("/db/api/thread/close/", methods = ['POST'])
def closeThread():
    logging.info("=====================================CLOSING THREAD BEGIN==========================================")
    try:
        thread = request.json["thread"]
    except:
        return json.dumps({"code": 2, "response": error_messages[2]})
    logging.info("  thread : " + str(thread))

    sql = "SELECT idThread FROM Thread WHERE idThread = %s"
    cursor.execute(sql, [thread])
    data = cursor.fetchone()
    if (not data):
        logging.info("=====================================CLOSING THREAD END WITHOUT DATA===============================\n")
        return json.dumps({"code": 1, "response": error_messages[1]})

    sql = "UPDATE Thread SET isClosed = 1 WHERE idThread = %s"
    cursor.execute(sql, [thread])

    response = json.dumps({"code": 0, "response": thread})
    logging.info("  Response : ")
    logging.info(response)
    logging.info("=====================================CLOSING THREAD END============================================\n")
    return response
    
@app.route("/db/api/thread/details/", methods = ['GET'])
def threadDetails():
    logging.info("===================THREAD DETAILS BEGIN=====================\n==========================================================")

    try:
        thread = request.args.get("thread")
    except:
        return json.dumps({"code": 2, "response": error_messages[2]})
    try:
        related = request.args.getlist("related")
    except:
        logging.info("  related is empty")
        related = []
    logging.info("  related : ")
    logging.info(related)
    if not entryRelatedInRightValues(related, ["user", "forum"]):
        return json.dumps({"code": 3, "response": error_messages[3]})
    related = []
    answer = getThreadDetailsByID(thread, related)
    if not answer:
        return json.dumps({"code": 1, "response": error_messages[1]})
    response = json.dumps({ "code": 0, "response": answer})
    logging.info("  RESPONSE : ")
    logging.info(response)
    logging.info("===================THREAD DETAILS END=====================\n==========================================================\n")
    return response
    
@app.route("/db/api/thread/list/", methods = ['GET'])
def threadsList():
    logging.info("=====================================THREAD LIST BEGIN============================================")
    try:
        user = request.args.get("user")
        logging.info("User : " + user)
    except:
        user = None
    try:
        forum = request.args.get("forum")
        logging.info("Forum : " + forum)
    except:
        forum = None

    if not user and not forum:
        return json.dumps({"code": 2, "response": error_messages[2]})

    limit   = getOptionalGetParameterOrDefault(request.args, "limit", None)
    order   = getOptionalGetParameterOrDefault(request.args, "order", "desc")
    since   = getOptionalGetParameterOrDefault(request.args, "since", None)

    sql = "SELECT * FROM Thread WHERE 1 = 1 "
    params = []
    if user:
        sql = sql + " AND idAuthor = %s"
        idAuthor = getUserIdByEmail(user)
        params.append(idAuthor)
    if forum:
        sql = sql + " AND idForum = %s"
        idForum = getForumIdByShortName(forum)
        params.append(idForum)
    if since:
        sql = sql + " AND DATE(date) >= %s" #TODO optimizate date query
        params.append(since)
    sql = sql + " ORDER BY date " + order
    if limit:
        sql = sql + " LIMIT " + str(limit)
    logging.info("FINAL SQL    = " + sql)
    logging.info("FINAL PARAMS = " + str(params))

    cursor.execute(sql, params)
    data = cursor.fetchall()
    answer = []
    for item in data:
        answer.append(getThreadDetailsByID(item[0], []))
    response = json.dumps({"code": 0, "response": answer})
    logging.info("Response : ")
    logging.info(response)
    logging.info("=====================================THREAD LIST END============================================")
    return response
    
@app.route("/db/api/thread/listPosts/", methods = ['GET'])
def threadListPosts():
    logging.info("THREAD LIST POSTS===========================")

    from Post import getListPostsOfThread
    thread  = None
    try:
        thread = int(request.args.get("thread"))
    except:
        return json.dumps({"code": 2, "response": error_messages[2]})

    limit = getOptionalGetParameterOrDefault(request.args, "limit", None)
    order = getOptionalGetParameterOrDefault(request.args, "order", "desc")
    since = getOptionalGetParameterOrDefault(request.args, "since", None)
    sort  = getOptionalGetParameterOrDefault(request.args, "sort ", "flat")
    logging.info("  thread  = " + str(thread))
    logging.info("  sort    = " + str(sort))

    answer = getListPostsOfThread(thread, since, order, limit)

    response = json.dumps({"code": 0, "response": answer})
    logging.info("  Response : ")
    logging.info(response)

    logging.info("THREAD LIST POSTS SUCCESSFUL================")
    return response
    
@app.route("/db/api/thread/open/", methods = ['POST'])
def openThread():
    if "thread" in request.json:
        thread = request.json["thread"]
    else:
        return json.dumps({"code": 2, "response": error_messages[2]})
    logging.info("  thread : " + str(thread))

    sql = "SELECT idThread FROM Thread WHERE idThread = %s"
    cursor.execute(sql, [thread])
    data = cursor.fetchone()
    if not data:
        logging.info("=====================================CLOSING THREAD END WITHOUT DATA===============================\n")
        return json.dumps({"code": 1, "response": error_messages[1]})

    sql = "UPDATE Thread SET isClosed = 0 WHERE idThread = %s"
    cursor.execute(sql, [thread])

    response = json.dumps({"code": 0, "response": thread})
    return response
    
@app.route("/db/api/thread/remove/", methods = ['POST'])
def removeThread():
    from Post import removePostsOfThread
    if "thread" in request.json:
        logging.info("REMOVING THREAD")

        thread = request.json["thread"]
    else:
        return json.dumps({"code": 2, "response": error_messages[2]})

    sql = "SELECT idThread FROM Thread WHERE idThread = %s"
    cursor.execute(sql, [thread])

    if cursor.fetchone() is None:
        return json.dumps({"code": 1, "response": error_messages[1]})

    removePostsOfThread(thread)

    sql = "UPDATE Thread SET isDeleted = 1 WHERE idThread = %s"
    cursor.execute(sql, [thread])

    response = json.dumps({ "code": 0, "response": {"thread": thread}})
    logging.info("REMOVING THREAD SUCCESSFULL\n")
    return response
    
@app.route("/db/api/thread/restore/", methods = ['POST'])
def restoreThread():
    from Post import restorePostsOfThread
    if "thread" in request.json:
        logging.info("RESTORING THREAD")

        thread = request.json["thread"]
    else:
        return json.dumps({"code": 2, "response": error_messages[2]})

    sql = "SELECT idThread FROM Thread WHERE idThread = %s"
    cursor.execute(sql, [thread])

    if cursor.fetchone() is None:
        return json.dumps({"code": 1, "response": error_messages[1]})

    restorePostsOfThread(thread)

    sql = "UPDATE Thread SET isDeleted = 0 WHERE idThread = %s"
    cursor.execute(sql, [thread])

    response = json.dumps({ "code": 0, "response": {"thread": thread}})
    logging.info("REMOVING THREAD SUCCESSFULL\n")
    return response
    
@app.route("/db/api/thread/subscribe/", methods = ['POST'])
def subscribeThread():
    logging.info("=======================SUBSCRIBE THREAD======================")
    try:
        user = request.json["user"]
        thread = request.json["thread"]
    except:
        return json.dumps({"code": 2, "response": error_messages[2]})
    idUser = getUserIdByEmail(user)
    if not idUser:
        return json.dumps({"code": 1, "response": error_messages[1]})

    logging.info("  User : " + str(idUser) + "; idThread : " + str(thread))
    sql = "INSERT INTO Subscription(idUser, idThread) VALUES(%s,%s)"
    try:
        cursor.execute(sql, [idUser, thread])
    except:
        return json.dumps({"code": 5, "response": error_messages[5]})

    response = json.dumps({"code": 0, "response": {"thread": thread, "user": user}})
    logging.info("  Result : " + response)
    logging.info("=======================SUBSCRIBE THREAD SUCCESS======================")
    return response
    
@app.route("/db/api/thread/unsubscribe/", methods = ['POST'])
def unsubscribeThread():
    logging.info("=====================UNSUBSCRIBE THREAD======================")

    try:
        user = request.json["user"]
        thread = request.json["thread"]
    except:
        return json.dumps({"code": 2, "response": error_messages[2]})

    idUser = getUserIdByEmail(user)
    if not idUser:
        return json.dumps({"code": 1, "response": error_messages[1]})

    logging.info("  User : " + str(idUser) + "; idThread : " + str(thread))

    sql = "DELETE FROM Subscription WHERE idUser = %s AND idThread = %s"
    cursor.execute(sql, [idUser, thread])

    response = json.dumps({"code": 0, "response": {"thread": thread, "user": user}})
    logging.info("  Result : " + response)
    logging.info("=====================UNSUBSCRIBE THREAD SUCCESS======================")
    return response
    
@app.route("/db/api/thread/update/", methods = ['POST'])
def updateThread():
    logging.info("=======================UPDATE THREAD==========================")
    try:
        message = request.json["message"]
        slug = request.json["slug"]
        thread = request.json["thread"]
    except:
        return json.dumps({"code": 2, "response": error_messages[2]})

    sql = "UPDATE Thread SET message = %s, slug = %s WHERE idThread = %s"
    cursor.execute(sql, [message, slug, thread])

    answer = getThreadDetailsByID(thread, [])
    response = json.dumps({"code": 0, "response": answer})
    logging.info("=======================UPDATE THREAD SUCCESS==================")

    return response
    
@app.route("/db/api/thread/vote/", methods = ['POST'])
def voteThread():
    logging.info("================THREAD VOTE=====================")

    if "vote" in request.json and "thread" in request.json:
        vote = request.json["vote"]
        thread = request.json["thread"]
    else:
        return json.dumps({"code": 2, "response": error_messages[2]})

    logging.info("  vote : " + str(vote) + ";  thread : " + str(thread))

    if vote == 1:
        addition = " likes = likes + 1"
    elif vote == -1:
        addition = " dislikes = dislikes + 1"
    else:
        logging.info("  incorrect vote param : " + str(vote))
        return json.dumps({"code": 2, "response": error_messages[2]})

    sql = "UPDATE Thread SET" + addition + " WHERE idThread = %s"
    cursor.execute(sql, [thread])

    answer = getThreadDetailsByID(thread, [])

    response = json.dumps({"code": 0, "response": answer})
    logging.info("  Response: ")
    logging.info(response)
    logging.info("================THREAD VOTE END=================")

    return response

def getThreadDetailsByID(threadID, related):
    sql = "SELECT * FROM Thread WHERE idThread = %s"
    cursor.execute(sql, [threadID])
    data = cursor.fetchone()
    if (not data):
        logging.info("Thread not found")
        return None
    try:
        sql = "SELECT count(*) FROM Post WHERE idThread = %s AND isDeleted = 0"
        cursor.execute(sql, [threadID])
        count_posts = cursor.fetchone()[0]
        logging.info("      Count posts of thread " + str(threadID) + " is " + str(count_posts))
    except:
        count_posts = 0
    answer = {}
    answer["id"] = data[0]
    answer["title"] = data[1]
    answer["message"] = data[2]
    answer["slug"] = data[3]
    answer["date"] = str(data[4])
    answer["isClosed"] = data[5]
    answer["isDeleted"] = data[6]
    forum_details = getForumDetailsById(data[7])
    answer["forum"] = forum_details["short_name"]
    answer["user"] = getUserEmailByID(data[8])
    answer["likes"] = data[9]
    answer["dislikes"] = data[10]
    answer["posts"] = count_posts
    answer["points"] = answer["likes"] - answer["dislikes"]
    if "user" in related:
        data_user = getUserInfoByEmail(answer["user"])
        answer["user"] = data_user
    if "forum" in related:
        data_forum = getForumDetailsByShortName(answer["forum"])
        answer["forum"] = data_forum
    logging.info("      ===========Answer getThreadByID() : ")
    logging.info(answer)
    logging.info("      ===================================\n")
    return answer

def getListThreadsOfForum(forum, since, order, limit, related):
    sql = "SELECT * FROM Thread WHERE idForum = %s"
    idForum = getForumIdByShortName(forum)
    params = [idForum]
    if since is not None:
        sql += " AND date >= %s"
        params.append(since)

    if order is not None:
        sql += " ORDER BY date " + order

    if limit is not None:
        sql += " LIMIT %s"
        params.append(int(limit))

    logging.info("      Final SQL    listThreads : " + sql)
    logging.info("      Final PARAMS listThreads : " + str(params))

    cursor.execute(sql, params)
    dictionary = cursor.fetchall()
    return getArrayThreadsFromDDictionary(dictionary, related)

def getArrayThreadsFromDDictionary(dictionary, related):
    array = []
    for item in dictionary:
        try:
            threadID = item[0]
            sql = "SELECT count(*) FROM Post WHERE idThread = %s AND isDeleted = 0"
            cursor.execute(sql, [threadID])
            count_posts = cursor.fetchone()[0]
            logging.info("      Count posts of thread " + str(threadID) + " is " + str(count_posts))
        except:
            count_posts = 0

        answer = {}
        answer["id"] = item[0]
        answer["title"] = item[1]
        answer["message"] = item[2]
        answer["slug"] = item[3]
        answer["date"] = str(item[4])
        answer["isClosed"] = item[5]
        answer["isDeleted"] = item[6]
        answer["forum"] = getForumShortNameById(item[7])
        answer["user"] = getUserEmailByID(item[8])
        answer["likes"] = item[9]
        answer["dislikes"] = item[10]
        answer["posts"] = count_posts
        answer["points"] = answer["likes"] - answer["dislikes"]
        if "user" in related:
            answer["user"] = getUserInfoByEmail(answer["user"])
        if "forum" in related:
            answer["forum"] = getForumDetailsByShortName(answer["forum"])
        array.append(answer)
    return array