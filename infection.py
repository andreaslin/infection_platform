#!/usr/bin ptyhon
# -*- coding: utf-8 -*-
from collections import deque
import json

class Platform:
    def __init__(self, file, type = 'total', verbose = False):
        self.__type = type
        self.__database = Database(file)

    def addUser(self, name, version = 0):
        self.__database.createUser(name, version)

    def infection(self, id, version):
        queue = deque([id])
        while(queue):
            user = self.__database.getUserById(queue.popleft())
            user.setVersion(version)
            infected = (user.getCoaching() | user.getCoacedhBy())
            for student in self.__database.getUsersWithId(infected):
                if(student.getVersion() != version):
                    queue.append(student.getId())

    def limitedInfection(self, id, version):
        pass

    def printAllUsers(self):
        print "user id\t\tname\t\t\tversion"
        for id, user in self.__database.getAllUsers().iteritems():
            print str(user.getId()) + "\t\t",
            print user.getName() + "\t\t\t",
            print str(user.getVersion()) + "\t\t"


class Database:
    def __init__(self, file):
        self.__users_list = dict()
        self.__MAX_NUMBER_OF_USERS = 1000000
        with open(file) as fh:
            json_list = json.load(fh)
            for elem in json_list:
                user = self.createUser(elem["id"], elem["name"], elem["version"])
                coaching_list = elem["coaching_list"]
                user.addStudents(coaching_list)

            for cid, user in self.__users_list.iteritems():
                for student in user.getCoaching():
                    self.__users_list[student].addCoach(cid)

    def createUser(self, uid, name, version = 0):
        user = User(uid, name, version)
        self.__addUser(user)
        return user

    def __addUser(self, user):
        self.__users_list[user.getId()] = user

    def removeUser(self, user):
        self.__users_list[user.getId()] = None

    def getUserById(self, uid):
        return self.__users_list[uid]

    def getUsersWithId(self, id_list):
        return map(lambda x: self.__users_list[x], id_list)

    def getAllUsers(self):
        return self.__users_list


class User:
    def __init__(self, uid, name, version = 0):
        self.__uid = uid
        self.__name = name
        self.__version = version
        self.__coaching = set()
        self.__coached_by = set()

    def getId(self):
        return self.__uid

    def getVersion(self):
        return self.__version

    def setVersion(self, version):
        self.__version = version

    def getName(self):
        return self.__name

    def getCoaching(self):
        return self.__coaching

    def getCoacedhBy(self):
        return self.__coached_by

    def addStudent(self, student_id):
        self.__coaching.add(student_id)

    def addStudents(self, student_id_list):
        self.__coaching |= set(student_id_list)

    def addCoach(self, coach_id):
        self.__coached_by.add(coach_id)
