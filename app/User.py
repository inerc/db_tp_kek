from app import app, cursor
from flask import request, jsonify
from functions import *
import json
import Forum

@app.route("/db/api/user/create/", methods = ['POST'])
def createUser():
    logging.info("================USER CREATION")
    try:
        email    = request.json["email"]
    except:
        return json.dumps({"code": 2, "response": error_messages[2]})

    try:
        name     = request.json["name"]
    except:
        name     = None
        logging.info("NAME IS None")
        logging.info("_____________________")
    try:
        username = request.json["username"]
    except:
        username = None
        logging.info("USERNAME IS None")
        logging.info("_____________________")
    try:
        about    = request.json["about"]
    except:
        about    = None
        logging.info("ABOUT IS None")
        logging.info("_____________________")

    if (not isString([name, email, username, about])):
        logging.info("one or more params not string")
        return json.dumps({"code": 2, "response": error_messages[2]})

    sql = "SELECT idUser FROM User WHERE email = %s"
    cursor.execute(sql, [email])
    if (cursor.fetchone() != None):
        logging.info(email + " is already exists")
        return json.dumps({"code": 5, "response": error_messages[5]})

    isAnonymous = False
    if ("isAnonymous" in request.json):
        isAnonymous = request.json["isAnonymous"]

    sql = "INSERT INTO User(username, email, name, about, isAnonymous) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, [username, email, name, about, isAnonymous])

    sql = "SELECT MAX(idUser) FROM User"
    cursor.execute(sql)
    idU = cursor.fetchone()[0]

    data = {}
    data['about'] = about
    data['email'] = email
    data['id'] = idU
    data['isAnonymous'] = isAnonymous
    data['name'] = name
    data['username'] = username
    answer = {"code": 0, "response": data}
    response = json.dumps(answer)
    logging.info("================SUCCESSFUL USER CREATION\n")
    return response

@app.route("/db/api/user/details/", methods = ['GET'])
def userDetails():
    try:
        email = request.args.get("user")
    except:
        return json.dumps({"code": 2, "response": error_messages[2]})
    logging.info(email)
    if (not isString([email])):
        return json.dumps({"code": 2, "response": error_messages[2]})

    answer = getUserInfoByEmail(email)
    if answer != None:
        return json.dumps({"code": 0, "response": answer})
    else:
        return json.dumps({"code": 1, "response": error_messages[1]})


@app.route("/db/api/user/follow/", methods = ['POST'])
def follow():
    logging.info("================USER FOLLOW========================")
    try:
        follower = request.json["follower"]
        followee = request.json["followee"]
    except:
        return json.dumps({"code": 2, "response": error_messages[2]})
    try:
        idFollower = getUserIdByEmail(follower)
        idFollowee = getUserIdByEmail(followee)
    except:
        return json.dumps({"code": 1, "response": error_messages[1]})

    logging.info("  follower : " + str(idFollower))
    logging.info("  followee : " + str(idFollowee))

    sql = "INSERT INTO Follower(idFollower, idFollowing) VALUES(%s, %s)"

    try:
        cursor.execute(sql, [idFollower, idFollowee])
    except:
        json.dumps({"code": 5, "response": error_messages[5]})


    emailsFollowers = getFollowerEmails(idFollower, None, None, None)
    emailsFollowing = getFollowingEmails(idFollower, None, None, None)

    userInfo = getUserInfoByID(idFollower)
    userInfo["followers"] = emailsFollowers
    userInfo["following"] = emailsFollowing
    userInfo["subscriptions"] = []
    logging.info("Response : ")
    logging.info(userInfo)
    response = json.dumps({"code": 0, "response": userInfo})
    logging.info("================USER FOLLOW SUCCESS================\n")
    return response

@app.route("/db/api/user/listFollowers/", methods = ['GET'])
def listFollowers():
    logging.info("================USER listFollowers========================")
    try:
        user = request.args.get("user")
    except:
        return json.dumps({"code": 2, "response": error_messages[2]})

    limit = getOptionalGetParameterOrDefault(request.args, "limit", None)
    order = getOptionalGetParameterOrDefault(request.args, "order", "desc")
    since = getOptionalGetParameterOrDefault(request.args, "since_id", None)

    logging.info("user : " + user)

    user_id = getUserIdByEmail(user)
    if not user_id:
        return json.dumps({"code": 1, "response": error_messages[1]})

    emails = getFollowerEmails(user_id, since, order, limit)

    answer = []
    for email in emails:
        user_by_email = getUserInfoByEmail(email)
        answer.append((user_by_email))

    response = json.dumps({ "code": 0, "response": answer })
    logging.info("Response : ")
    logging.info(response)
    logging.info("================USER listFollowers END====================\n")
    return response

@app.route("/db/api/user/listFollowing/", methods = ['GET'])
def listFollowing():
    logging.info("================USER listFollowing========================")
    try:
        user = request.args.get("user")
    except:
        return json.dumps({"code": 2, "response": error_messages[2]})

    limit = getOptionalGetParameterOrDefault(request.args, "limit", None)
    order = getOptionalGetParameterOrDefault(request.args, "order", "desc")
    since = getOptionalGetParameterOrDefault(request.args, "since_id", None)

    logging.info("  User : " + user)

    user_id = getUserIdByEmail(user)
    if not user_id:
        return json.dumps({"code": 1, "response": error_messages[1]})

    emails = getFollowingEmails(user_id, since, order, limit)

    answer = []
    for email in emails:
        user_by_email = getUserInfoByEmail(email)
        answer.append((user_by_email))

    response = json.dumps({ "code": 0, "response": answer })
    logging.info("Response : ")
    logging.info(response)
    logging.info("================USER listFollowing END====================\n")
    return response

@app.route("/db/api/user/listPosts/", methods = ['GET'])
def userListPosts():
    logging.info("================USER LISTPOSTS================")
    try:
        user = request.args.get("user")
    except:
        return json.dumps({"code": 2, "response": error_messages[2]})

    limit = getOptionalGetParameterOrDefault(request.args, "limit", None)
    order = getOptionalGetParameterOrDefault(request.args, "order", "desc")
    since = getOptionalGetParameterOrDefault(request.args, "since", None)

    idUser = getUserIdByEmail(user)
    if not idUser:
        return json.dumps({"code": 1, "response": error_messages[1]})

    sql = "SELECT P.* FROM Post P INNER JOIN User U ON P.idAuthor = U.idUser WHERE U.idUser = %s"
    params = [idUser]

    if since:
        params.append(since)
        sql += " AND P.date >= %s"

    sql += " ORDER BY P.date " + order

    if limit:
        params.append(int(limit))
        sql += " LIMIT %s"

    logging.info("  Final SQL    listPosts : " + sql)
    logging.info("  Final PARAMS listPosts : " + str(params))

    cursor.execute(sql, params)
    result = getArrayDictFromDoubleDictionary(cursor.fetchall())
    logging.info("  Results : ")

    response = json.dumps({ "code": 0, "response": result})
    logging.info("  Response : " + response)
    logging.info("================USER LISTPOSTS END============")
    return response

@app.route("/db/api/user/unfollow/", methods = ['POST'])
def unfollow():
    logging.info("================USER UNFOLLOW========================")
    try:
        follower = request.json["follower"]
        followee = request.json["followee"]
    except:
        return json.dumps({"code": 2, "response": error_messages[2]})
    try:
        idFollower = getUserIdByEmail(follower)
        idFollowee = getUserIdByEmail(followee)
    except:
        return json.dumps({"code": 1, "response": error_messages[1]})

    logging.info("  follower : " + str(idFollower))
    logging.info("  followee : " + str(idFollowee))

    sql = "DELETE FROM Follower WHERE idFollower = %s AND idFollowing = %s"
    cursor.execute(sql, [idFollower, idFollowee])
    answer = getUserInfoByID(idFollower)

    response = json.dumps({"code": 0, "response": answer})
    logging.info("================USER UNFOLLOW END====================")
    return response

@app.route("/db/api/user/updateProfile/", methods = ['POST'])
def updateProfile():
    logging.info("=======================UPDATING PROFILE========================")
    try:
        about = request.json["about"]
        user = request.json["user"]
        name = request.json["name"]
    except:
        logging.error("  no required fields")
        return json.dumps({"code": 2, "response": error_messages[2]})
    sql = "UPDATE User SET about = %s, name = %s WHERE email = %s"
    cursor.execute(sql, [about, name, user])
    result = getUserInfoByEmail(user)

    response = json.dumps({"code": 0, "response": result})
    logging.info("  Result : " + response)
    logging.info("=======================UPDATING PROFILE SUCCESSFUL=============")
    return response

def getUserInfoByEmail(email):
    sql = "SELECT * FROM User WHERE email = %s"
    cursor.execute(sql, [email])

    q_result = cursor.fetchone()

    if (q_result != None):
        data = {}
        data["id"] = q_result[0]
        data["username"] = q_result[1]
        data["email"] = q_result[2]
        data["name"] = q_result[3]
        data["about"] = q_result[4]
        data["isAnonymous"] = q_result[5]
        data["followers"] = getFollowerEmails(data["id"], None, None, None)
        data["following"] = getFollowingEmails(data["id"], None, None, None)
        data["subscriptions"] = getSubscriptions(data["id"])
        return data
    else:
        return None

def getUserIdByEmail(email):
    logging.info("      getting user by email : ")
    sql = "SELECT idUser FROM User WHERE email = %s"
    cursor.execute(sql, [email])
    q_result = cursor.fetchone()[0]
    logging.info("      getted user by email : " + str(q_result))
    return q_result

def getUserInfoByID(id):
    sql = "SELECT * FROM User WHERE idUser = %s"
    cursor.execute(sql, [id])

    q_result = cursor.fetchone()

    if (q_result != None):
        data = {}
        data["id"] = q_result[0]
        data["username"] = q_result[1]
        data["email"] = q_result[2]
        data["name"] = q_result[3]
        data["about"] = q_result[4]
        data["isAnonymous"] = q_result[5]
        data["followers"] = getFollowerEmails(data["id"], None, None, None)
        data["following"] = getFollowingEmails(data["id"], None, None, None)
        data["subscriptions"] = getSubscriptions(data["id"])
        return data
    else:
        return None

def getUserEmailByID(id):
    sql = "SELECT email FROM User WHERE idUser = %s"
    cursor.execute(sql, [id])

    q_result = cursor.fetchone()

    if (q_result != None):
        return q_result[0]
    else:
        return None

def getFollowerEmails(idUser, since, order, limit):
    logging.info("")
    sql = "SELECT U.email FROM Follower F INNER JOIN User U ON F.idFollower = U.idUser WHERE F.idFollowing = %s"
    params = [idUser]
    if since:
        sql += " AND U.idUser > %s"
        params.append(int(since))
    if not order:
        order = "desc"
    sql += " ORDER BY U.username " + order

    if limit:
        sql += " LIMIT %s"
        params.append(int(limit))
    logging.info("      Final SQL    followerEmails : " + sql)
    logging.info("      Final PARAMS followerEmails : " + str(params))
    cursor.execute(sql, params)
    emails = getArrayEmailsFromDoubleDictionary(cursor.fetchall())
    logging.info("      EMAILS FOLLOWERS OF USER (" + str(idUser) + ") : " + str(emails))
    logging.info("")
    return emails

def getFollowingEmails(idUser, since, order, limit):
    sql = "SELECT U.email FROM Follower F INNER JOIN User U ON F.idFollowing = U.idUser WHERE F.idFollower = %s"
    params = [idUser]
    if since:
        sql += " AND U.idUser > %s"
        params.append(int(since))
    if not order:
        order = "desc"
    sql += " ORDER BY U.username " + order

    if limit:
        sql += " LIMIT %s"
        params.append(int(limit))
    logging.info("      Final SQL    followingEmails : " + sql)
    logging.info("      Final PARAMS followingEmails : " + str(params))
    cursor.execute(sql, params)
    emails = getArrayEmailsFromDoubleDictionary(cursor.fetchall())
    logging.info("      EMAILS FOLLOWING OF USER (" + str(idUser) + ") : " + str(emails))
    return emails

def getSubscriptions(idUser):
    sql = "SELECT idThread FROM Subscription WHERE idUser = %s"
    cursor.execute(sql, [idUser])

    subscriptions = getArrayEmailsFromDoubleDictionary(cursor.fetchall())
    logging.info("      Subscriptions of USER (" + str(idUser) + ") : " + str(subscriptions))
    return subscriptions

def getArrayEmailsFromDoubleDictionary(dictionary):
    array = []
    for item in dictionary:
        array.append(item[0])
    return array

def getArrayDictFromDoubleDictionary(dictionary):
    from Forum import getForumShortNameById

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
        logging.info("      dictionary item, : " + str(dict))
        array.append(dict)
    return array

def getArrayUsersFromDoubleDictionary(dictionary):
    array = []
    for item in dictionary:
        data = {}
        data["id"] = item[0]
        data["username"] = item[1]
        data["email"] = item[2]
        data["name"] = item[3]
        data["about"] = item[4]
        data["isAnonymous"] = item[5]
        data["followers"] = getFollowerEmails(data["id"], None, None, None)
        data["following"] = getFollowingEmails(data["id"], None, None, None)
        data["subscriptions"] = getSubscriptions(data["id"])
        logging.info("      dictionary item : " + str(dict))
        array.append(data)
    return array

# `idPost` INT NOT NULL AUTO_INCREMENT,
#   `parent` INT NULL DEFAULT NULL,
#   `isApproved` TINYINT(1) NULL DEFAULT FALSE,
#   `isHighlighted` TINYINT(1) NULL DEFAULT FALSE,
#   `isEdited` TINYINT(1) NULL DEFAULT FALSE,
#   `isSpam` TINYINT(1) NULL DEFAULT FALSE,
#   `isDeleted` TINYINT(1) NULL DEFAULT FALSE,
#   `likes` INT NOT NULL,
#   `dislikes` INT NOT NULL,
#   `date` DATETIME NOT NULL,
#   `message` TEXT NOT NULL,
#   `idForum` INT NOT NULL,
#   `idThread` INT NOT NULL,
#   `idAuthor` INT NOT NULL,

def getListUsersOfForum(forum, since, order, limit):
    from Forum import getForumIdByShortName
    sql = "SELECT DISTINCT U.* FROM User U INNER JOIN Post P ON U.idUser = P.idAuthor WHERE P.idForum = %s"
    idForum = getForumIdByShortName(forum)
    params = [idForum]
    if since:
        sql += " AND U.idUser >= %s"
        params.append(int(since))

    logging.info("      order = " + order)

    sql += " ORDER BY U.name " + order

    if limit:
        sql += " LIMIT %s"
        params.append(int(limit))

    logging.info("      Final SQL    followerEmails : " + sql)
    logging.info("      Final PARAMS followerEmails : " + str(params))
    cursor.execute(sql, params)
    array = getArrayUsersFromDoubleDictionary(cursor.fetchall())
    logging.info("      LIST USERES OF FORUM (" + str(idForum) + ") : " + str(array))
    return array