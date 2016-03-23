from app import app, cursor
from functions import *
from User import *
from Forum import *
from Thread import *
from flask import request
import json

@app.route("/db/api/post/create/", methods = ['POST'])
def createPost():
    logging.info("================Post CREATION\n")
    logging.info("Request : ")
    logging.info(request.json)
    logging.info(request.json["thread"])
    try:
        thread = request.json["thread"]
        message = request.json["message"]
        date = request.json["date"]
        user = request.json["user"]
        forum = request.json["forum"]
        logging.info("Thread : " + str(thread))
        logging.info("Message : " + message)
        logging.info("Date : " + str(date))
        logging.info("User : " + str(user))
        logging.info("Forum : " + str(forum))

    except:
        return json.dumps({"code": 2, "response": error_messages[2]})

    parent        = getOptionalParameterOrDefault(request.json, "parent", None)
    isApproved    = getOptionalParameterOrDefault(request.json, "isApproved", False)
    isHighlighted = getOptionalParameterOrDefault(request.json, "isHighlighted", False)
    isEdited      = getOptionalParameterOrDefault(request.json, "isEdited", False)
    isSpam        = getOptionalParameterOrDefault(request.json, "isSpam", False)
    isDeleted     = getOptionalParameterOrDefault(request.json, "isDeleted", False)

    try:
        id_Forum = getForumDetailsByShortName(forum)["id"]
        id_User = getUserInfoByEmail(user)["id"]
    except:
        return json.dumps({"code": 2, "response": error_messages[2]})

    sql = "INSERT INTO Post(parent, isApproved, isHighlighted, isEdited, isSpam, isDeleted, likes, dislikes, date, message, idForum, idThread, idAuthor) " \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql,    [parent, isApproved, isHighlighted, isEdited, isSpam, isDeleted,     0,        0, date, message, id_Forum,  thread, id_User])

    sql = "SELECT MAX(idPost) FROM Post"
    cursor.execute(sql)
    idP = cursor.fetchone()[0]

    answer = {}
    answer["id"] = idP
    answer["parent"] = parent
    answer["isApproved"] = isApproved
    answer["isHighlighted"] = isHighlighted
    answer["isEdited"] = isEdited
    answer["isSpam"] = isSpam
    answer["isDeleted"] = isDeleted
    answer["likes"] = 0
    answer["dislikes"] = 0
    answer["points"] = answer["likes"] - answer["dislikes"]
    answer["date"] = date
    answer["message"] = message
    answer["forum"] = forum
    answer["thread"] = thread
    answer["user"] = user
    response = json.dumps({"code": 0, "response": answer})
    logging.info("  Response : " + response)
    logging.info("================SUCCESSFUL Post CREATION\n")
    return response

@app.route("/db/api/post/details/", methods = ['GET'])
def postDetails():
    logging.info("===================POST DETAILS BEGIN=====================\n============================================================\n")

    try:
        post = request.args.get("post")
    except:
        return json.dumps({"code": 2, "response": error_messages[2]})
    try:
        related = request.args.getlist("related")
    except:
        logging.info("  related is empty")
        related = []
    related = []
    logging.info("related : ")
    logging.info(related)
    logging.info("post : ")
    logging.info(post)
    answer = getPostDetailsByID(post, related)
    if not answer:
        return json.dumps({"code": 1, "response": error_messages[1]})
    response = json.dumps({ "code": 0, "response": answer})
    logging.info("  RESPONSE : " + response)
    logging.info("===================POST DETAILS END=====================\n============================================================\n")
    return response
    
@app.route("/db/api/post/list/", methods = ['GET'])
def postsList():
    forum   = None
    thread  = None
    try:
        thread = int(request.args.get("thread"))
    except:
        try:
            forum = request.args.get("forum")
        except:
            return json.dumps({"code": 2, "response": error_messages[2]})

    limit = getOptionalGetParameterOrDefault(request.args, "limit", None)
    order = getOptionalGetParameterOrDefault(request.args, "order", "desc")
    since = getOptionalGetParameterOrDefault(request.args, "since", None)

    logging.info("  thread = " + str(thread))

    answer = {}
    if thread is not None:
        answer = getListPostsOfThread(thread, since, order, limit)

    if forum is not None:
        answer = getListPostsOfForum(forum, since, order, limit, [])


    response = json.dumps({"code": 0, "response": answer})
    return response

@app.route("/db/api/post/remove/", methods = ['POST'])
def removePost():
    if "post" in request.json:
        post = request.json["post"]
    else:
        return json.dumps({"code": 2, "response": error_messages[2]})

    sql = "SELECT idPost FROM Post WHERE idPost = %s"
    cursor.execute(sql, [post])
    result = cursor.fetchone()
    if not result:
        return json.dumps({"code": 1, "response": error_messages[1]})

    sql = "UPDATE Post SET isDeleted = 1 WHERE idPost = %s"
    cursor.execute(sql, [post])

    response = json.dumps({"code": 0, "response": post})
    return response
    
@app.route("/db/api/post/restore/", methods = ['POST'])
def restorePost():
    if "post" in request.json:
        post = request.json["post"]
    else:
        return json.dumps({"code": 2, "response": error_messages[2]})

    sql = "SELECT idPost FROM Post WHERE idPost = %s"
    cursor.execute(sql, [post])
    result_arr = cursor.fetchone()
    result = result_arr[0]
    if not result:
        return json.dumps({"code": 1, "response": error_messages[1]})

    sql = "UPDATE Post SET isDeleted = 0 WHERE idPost = %s"
    cursor.execute(sql, [post])

    response = json.dumps({"code": 0, "response": post})
    return response
    
@app.route("/db/api/post/update/", methods = ['POST'])
def updatePost():
    logging.info("  Updating post")
    if "post" in request.json and "message" in request.json:
        post = request.json["post"]
        message = request.json["message"]
    else:
        return json.dumps({"code": 2, "response": error_messages[2]})

    sql = "SELECT idPost FROM Post WHERE idPost = %s"
    cursor.execute(sql, [post])
    result_arr = cursor.fetchone()
    result = result_arr[0]
    if not result:
        return json.dumps({"code": 1, "response": error_messages[1]})

    sql = "UPDATE Post SET message = %s WHERE idPost = %s"
    cursor.execute(sql, [message, post])
    response = json.dumps({"code": 0, "response": post})
    logging.info("  Post " + str(post) + (" is updated successfully\n"))
    return response
    
@app.route("/db/api/post/vote/", methods = ['POST'])
def votePost():
    logging.info("================POST VOTE=====================")

    if "vote" in request.json and "post" in request.json:
        vote = request.json["vote"]
        post = request.json["post"]
    else:
        return json.dumps({"code": 2, "response": error_messages[2]})

    logging.info("  vote : " + str(vote) + ";  post : " + str(post))

    if vote == 1:
        addition = " likes = likes + 1"
    elif vote == -1:
        addition = " dislikes = dislikes + 1"
    else:
        logging.info("  incorrect vote param : " + str(vote))
        return json.dumps({"code": 2, "response": error_messages[2]})

    sql = "UPDATE Post SET" + addition + " WHERE idPost = %s"
    cursor.execute(sql, [post])

    answer = getPostDetailsByID(post, [])

    response = json.dumps({"code": 0, "response": answer})
    logging.info("  Response: ")
    logging.info(response)
    logging.info("================POST VOTE END=================")

    return response

def getPostDetailsByID(postID, related):
    sql = "SELECT * FROM Post WHERE idPost = %s"
    cursor.execute(sql, [postID])
    data = cursor.fetchone()
    logging.info(data)
    if (not data):
        logging.info("      Thread not found")
        return None
    answer = {}
    answer["id"] = data[0]
    answer["parent"] = data[1]
    answer["isApproved"] = data[2]
    answer["isHighlighted"] = data[3]
    answer["isEdited"] = data[4]
    answer["isSpam"] = data[5]
    answer["isDeleted"] = data[6]
    answer["likes"] = data[7]
    answer["dislikes"] = data[8]
    answer["date"] = str(data[9])
    answer["message"] = data[10]
    answer["forum"] = getForumShortNameById(data[11])
    answer["thread"] = data[12]
    answer["user"] = getUserEmailByID(data[13])
    answer["points"] = answer["likes"] - answer["dislikes"]

    if "user" in related:
        data_user = getUserInfoByEmail(answer["user"])
        answer["user"] = data_user
    if "forum" in related:
        answer["forum"] = getForumDetailsByShortName(answer["forum"])
    if "thread" in related:
        answer["thread"] = getThreadDetailsByID(answer["thread"], [])
    logging.info("      ===========Answer getPostByID() : ")
    logging.info(answer)
    logging.info("      ===================================")
    return answer

def getListPostsOfThread(thread, since, order, limit):
    logging.info("      GETTING LIST POSTS BY THREAD")
    sql = "SELECT * FROM Post WHERE idThread = %s"
    params = [thread]
    if since:
        sql += " AND date >= %s"
        params.append(since)

    sql += " ORDER BY date " + order

    if limit:
        sql += " LIMIT %s"
        params.append(int(limit))

    logging.info("      Final SQL    listPosts : " + sql)
    logging.info("      Final PARAMS listPosts : " + str(params))

    cursor.execute(sql, params)
    result = cursor.fetchall()
    answer = getArrayPostsFormDDictionary(result, [])

    logging.info("      GETTED POSTS : ")
    logging.info(answer)
    logging.info("      ==============")

    return answer

def getListPostsOfForum(forum, since, order, limit, related):
    logging.info("      GETTING LIST POSTS BY FORUM")
    idForum = getForumIdByShortName(forum)
    sql = "SELECT * FROM Post WHERE idForum = %s"
    params = [idForum]
    if since:
        sql += " AND date >= %s"
        params.append(since)

    sql += " ORDER BY date " + order

    if limit:
        sql += " LIMIT %s"
        params.append(int(limit))

    logging.info("      Final SQL    listPosts : " + sql)
    logging.info("      Final PARAMS listPosts : " + str(params))

    cursor.execute(sql, params)
    result = cursor.fetchall()
    answer = getArrayPostsFormDDictionary(result, related)

    logging.info("      GETTED POSTS : ")
    logging.info(answer)
    logging.info("      ==============")

    return answer

def getArrayPostsFormDDictionary(dictionary, related):
    from Thread import getThreadDetailsByID
    from User import getUserInfoByEmail
    from Forum import  getForumDetailsByShortName
    array = []
    for item in dictionary:
        dict = {}
        dict["id"] = item[0]
        dict["parent"] = item[1]
        dict["isApproved"] = item[2]
        dict["isHighlighted"] = item[3]
        dict["isEdited"] = item[4]
        dict["isSpam"] = item[5]
        dict["isDeleted"] = item[6]
        dict["likes"] = item[7]
        dict["dislikes"] = item[8]
        dict["date"] = str(item[9])
        dict["message"] = item[10]
        dict["forum"] = getForumShortNameById(item[11])
        dict["thread"] = item[12]
        dict["user"] = getUserEmailByID(item[13])
        dict["points"] = dict["likes"] - dict["dislikes"]
        if "thread" in related:
            dict["thread"] = getThreadDetailsByID(dict["thread"], [])
        if "user" in related:
            dict["user"] = getUserInfoByEmail(dict["user"])
        if "forum" in related:
            dict["forum"] = getForumDetailsByShortName(dict["forum"])
        logging.info("      dictionary item, no message : " + str(dict))
        array.append(dict)
    return array

def removePostsOfThread(thread):
    logging.info("      removing posts")
    sql = "UPDATE Post SET isDeleted = 1 WHERE idThread = %s"
    cursor.execute(sql, [thread])

def restorePostsOfThread(thread):
    logging.info("      restoring posts")
    sql = "UPDATE Post SET isDeleted = 0 WHERE idThread = %s"
    cursor.execute(sql, [thread])