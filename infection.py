#!/usr/bin ptyhon
# -*- coding: utf-8 -*-
from collections import deque
from graphviz import Digraph
import json

class Platform:
    def __init__(self, file, verbose = False):
        self.__database = Database(file)
        self.__file_name = file.split('.')[0]

    def addUser(self, name, version = 0):
        return self.__database.createUser(name, version)

    def removeUserById(self, uid):
        self.__database.removeUserById(uid)

    def getUserById(self, uid):
        return self.__database.getUserById(uid)

    def infection(self, uid, version):
        # queue = deque([id])
        # while(queue):
        #     user = self.__database.getUserById(queue.popleft())
        #     user.setVersion(version)
        #     infected = (user.getCoaching() | user.getCoacedhBy())
        #     for infected_user in self.__database.getUsersWithId(infected):
        #         if(infected_user.getVersion() != version):
        #             queue.append(infected_user.getId())
        self.__database.setClusterWithVersion(
            self.__database.getUserById(uid).getClusterId(), version)

    def limitedInfection(self, uid, version, limit):
        for cid, cluster in enumerate(self.__database.getAllClusters()):
            if uid in cluster and len(cluster) <= limit:
                self.__database.setClusterWithVersion(cid, version)
                return True
        return False

    def printAllUsers(self):
        print "User Id" + '\t' * 2,
        print "Name" + '\t' * 4,
        print "Version" + '\t' * 2,
        print "Cluster Id"
        for id, user in self.__database.getAllUsers().iteritems():
            print str(user.getId()) + '\t' * 2,
            print user.getName() + '\t' * 3,
            print str(user.getVersion()) + '\t' * 2,
            print str(user.getClusterId())

    def generateGraph(self):
        g = Digraph('User Relationship', filename=self.__file_name + ".gv", format='png')
        for cid, cluster in enumerate(self.__database.getAllClusters()):
            temp = cluster.pop()
            version = self.__database.getUserById(temp).getVersion()
            cluster.add(temp)

            graph_cluster = Digraph(str(cid))
            for uid in cluster:
                user = self.__database.getUserById(uid)
                graph_cluster.node(str(uid))
                for coaching in user.getCoaching():
                    graph_cluster.node(str(coaching))
                    if uid != coaching:
                        graph_cluster.edge(str(uid), str(coaching))

            g.subgraph(graph_cluster)
        g.view()


# Cluster is defined as a group of users that are connected either by
# the coaching or coachby relationship. Infection will affect one cluster
# at a time.
class Database:
    def __init__(self, file):
        self.__users_list = dict()
        self.__users_clusters = []
        self.__MAX_NUMBER_OF_USERS = 1000000
        with open(file) as fh:
            json_list = json.load(fh)
            for elem in json_list:
                user = self.createUser(elem["id"], elem["name"], elem["version"])
                coaching_list = elem["coaching_list"]
                user.addStudents(coaching_list)

            # Build CoachedBy
            for cid, user in self.__users_list.iteritems():
                for student in user.getCoaching():
                    self.__users_list[student].addCoach(cid)

            # Build clusters
            self.__buildClusters()

    def createUser(self, uid, name, version = 0):
        user = User(uid, name, version)
        self.__addUser(user)
        return user

    def __addUser(self, user):
        self.__users_list[user.getId()] = user

    def removeUserById(self, uid):
        self.__users_list[uid] = None

    def getUserById(self, uid):
        return self.__users_list[uid]

    def getUsersWithIds(self, uid_list):
        return map(lambda x: self.__users_list[x], uid_list)

    def getAllUsers(self):
        return self.__users_list

    def getAllClusters(self):
        return self.__users_clusters

    def __buildClusters(self):
        for uid, user in self.__users_list.iteritems():
            self.__groupToCluster(set([user.getId()]) |
                                    user.getCoaching() |
                                    user.getCoacedhBy())

        # Assign cluster id to users
        for uid, user in self.__users_list.iteritems():
            i = 0
            while(i  < len(self.__users_clusters)):
                if uid in self.__users_clusters[i]:
                    user.setClusterId(i)
                i += 1

    def __groupToCluster(self, uid_set):
        new_cluster = True

        for i, cluster in enumerate(self.__users_clusters):
            if not cluster.isdisjoint(uid_set):
                cluster |= uid_set
                new_cluster = False

        # Combine overlapping clusters
        i = 0
        while(i < len(self.__users_clusters)):
            j = i + 1
            while(j < len(self.__users_clusters)):
                cluster_1 = self.__users_clusters[i]
                cluster_2 = self.__users_clusters[j]

                if not cluster_1.isdisjoint(cluster_2):
                    cluster_1 |= cluster_2
                    self.__users_clusters.pop(j)
                else:
                    j += 1
            i += 1

        # New cluster
        if new_cluster:
            self.__users_clusters.append(uid_set)

    def __updateCluster(self):
        # TODO: Update clusters after user is added or removed
        pass

    def setClusterWithVersion(self, cluster_id, version):
        map(lambda x: x.setVersion(version),
            self.getUsersWithIds(self.__users_clusters[cluster_id]))

class User:
    def __init__(self, uid, name, version = 0):
        self.__uid = uid
        self.__name = name
        self.__version = version
        self.__coaching = set()
        self.__coached_by = set()
        self.__cluster_id = 0

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

    def setClusterId(self, cid):
        self.__cluster_id = cid

    def getClusterId(self):
        return self.__cluster_id
