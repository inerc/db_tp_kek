# -*- coding: utf-8 -*-
from app import app, cursor
from functions import *
from flask import request
import json

@app.route("/db/api/forum/create/", methods = ['POST'])
def createForum():
    logging.info("================FORUM CREATION")
    # logging.info("REQUEST :")
    # logging.info(request.json)
    # logging.info("SH_NAME : " + request.json["short_name"])
    # logging.info("USER : " + request.json["user"])
    # logging.info("NAME : " + request.json["name"].encode("UTF-8"))
    try:
        name       = request.json["name"].encode("UTF-8")
        logging.info("NAME : " + name)
        short_name = request.json["short_name"]
        logging.info("SHORT_NAME : " + short_name)
        user       = request.json["user"]
        logging.info("USER : " + user)
    except:
        logging.info("error in parsing params")
        return json.dumps({"code": 2, "response": error_messages[2]})

    cursor.execute("SELECT idUser FROM User WHERE User.email = %s", [user])
    id_User = cursor.fetchone()
    if (not id_User):
        return json.dumps({"code": 1, "response": error_messages[1]})
    id_User = id_User[0]

   

    sql = "SELECT max(idForum) FROM Forum"
    cursor.execute(sql)
    idF = cursor.fetchone()[0]
    answer = {"code": 0, "response": {"id": idF, "name": name, "short_name":short_name, "user": user}}

    response = json.dumps(answer)
    logging.info("================SUCCESSFUL FORUM CREATION\n")
    return response
