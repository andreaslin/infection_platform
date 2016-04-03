#!/usr/bin ptyhon
# -*- coding: utf-8 -*-

import json
import sys
import random

def generateClusterList(json_list):
    random.seed()
    min_cluster_num = 1
    max_cluster_num = 100

    all_ids = range(len(json_list))
    random.shuffle(all_ids)

    count = 0
    clusters = []
    clusters_sets = []
    while(count < len(json_list)):
        size = random.randint(min_cluster_num, max_cluster_num)
        c = all_ids[:size+1]
        all_ids = all_ids[size+1:]
        clusters.append(c)
        clusters_sets.append(set(c))
        count += size

    return clusters, clusters_sets

def getClusterId(clusters_sets, uid):
    for i, cluster in enumerate(clusters_sets):
        if uid in cluster:
            return i

file_name = sys.argv[1]
json_list = None
with open(file_name) as fh:
    json_list = json.load(fh)
    clusters, clusters_sets = generateClusterList(json_list)

    for i in range(len(json_list)):
        cluster_id = getClusterId(clusters_sets, i)
        cluster_size = len(clusters[cluster_id])
        rand_size = random.randint(0, cluster_size / 2)
        rand_coaching = clusters[cluster_id][0:rand_size]
        clusters[cluster_id] = clusters[cluster_id][rand_size:]
        json_list[i]["coaching_list"] = rand_coaching

with open(file_name, 'w+') as fh:
    json.dump(json_list, fh, sort_keys=True, ensure_ascii=False, indent=2)
