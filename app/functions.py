# -*- coding: utf-8 -*-
from flask import request

import logging
f = open("myLog.log", "w")
f.close()
logging.basicConfig(filename='myLog.log', level=logging.DEBUG, format='%(message)s')

#сообщения к кодам ответов (код сообщения равен индексу в массиве)
error_messages = ["OK",
         "object not found",
         "incorrect query",
         "uncorrect semantic query",
         "undefined error",
         "already exists"]

#USER
def isString(args):
    for arg in args:
        if (not isinstance(arg, basestring)):
            if arg:
                return False
    return True

def getOptionalGetParameterOrDefault(args, param, default):
    try:
        data = args.get(param)
    except:
        data = default
    if data is None:
        data = default
    logging.info("      option GET parameter " + str(param) + " : " + str(data))
    return data
#POST
def getOptionalParameterOrDefault(json, param, default):
    if param in json:
        data = json[param]
    else:
        data = default
    logging.info("      option POST parameter " + str(param) + " : " + str(data))
    return data

def entryRelatedInRightValues(related, right):
    for item in related:
        if item not in right:
            logging.info("      " + str(item) + " not in " + str(right))
            return False
    return True