import requests
import mechanize
from bs4 import BeautifulSoup, Comment
import utility
import pickle
import time
import random

g_users = {}
g_used = {}

def combine(self_id):
    data1 = pickle.load(open(self_id + "_data_save1.p", "rb"))
    data2 = pickle.load(open(self_id + "_data_save2.p", "rb"))
    data3 = pickle.load(open(self_id + "_data_save3.p", "rb"))

    data_combined = []
    data_combined += data1[:-1]
    data_combined += data2[:-1]
    data_combined += data3
    data_combined = [x for x in data_combined if len(x[2]) > 1]
    # print len(data_combined)
    # print data_combined
    pickle.dump(data_combined, open(self_id + "_combined_data.p", "wb"))


def load_data(data_file):
    data = pickle.load(open(data_file, "rb"))
    data_limit = len(data)
    adj_list = {}
    users = {}
    for i in range(0, data_limit):
        c_users = [(k, v) for (k, v) in data[i][2].iteritems()]
        for (j_id, j_name) in c_users:
            users[j_id] = j_name.encode('utf8')
            # if not j_id in adj_list:
            #     adj_list[j_id] = {}
            # for (k_id, k_name) in c_users:
            #     if j_id != k_id:
            #         adj_list[j_id][k_id] = 0

    for k in users.keys():
        adj_list[k] = {}
        for k2 in users.keys():
            if k != k2:
                adj_list[k][k2] = 0

    for i in range(0, data_limit):
        c_users = [(k, v) for (k, v) in data[i][2].iteritems()]
        for (j_id, j_name) in c_users:
            for (k_id, k_name) in c_users:
                if j_id != k_id:
                    adj_list[j_id][k_id] += 1
                    adj_list[k_id][j_id] += 1

    for u_id in users.keys():
        tmp = sorted(adj_list[u_id].items(), key=lambda x: -x[1])
        tmp_dict = {}
        for (k, v) in tmp:
            tmp_dict[k] = v
        adj_list[u_id] = tmp_dict
        verbose = [(users[k], v) for (k, v) in tmp]
        # if u_id == self_id:
        #     print users[u_id], verbose
        # print

    return adj_list, users


def verbose_list(object):
    return [g_users[x] for x in object]


def verbose_dict(object):
    return [(g_users[k], v) for (k, v) in object]


def build_clique(clique, threshold, starting_threshold, users, adj_list, used):
    # print verbose_list(clique), threshold
    cur_id = clique[-1]
    used[cur_id] = 1
    friends = sorted(adj_list[cur_id].items(), key=lambda x: -x[1])

    new_threshold = threshold * 0.2
    if new_threshold < starting_threshold:
        new_threshold = starting_threshold
    if new_threshold < 3:
        new_threshold = 3

    for k, v in friends:
        if k not in clique and k not in used:
            if v >= new_threshold and v < threshold:
                # print users[k], v, threshold
                clique.append(k)
                clique, used = build_clique(clique, v, starting_threshold, users, adj_list, used)

    return clique, used


def analyse(self_id, users, adj_list):
    my_friends = sorted(adj_list[self_id].items(), key=lambda x: -x[1])
    verbose = [(users[k], v) for (k, v) in my_friends]
    used = {}
    # print verbose

    # Runs through all friends in decreasing order, make 1 call
    for (k, v) in my_friends:
        if k not in used:
            clique, build_used = build_clique([self_id, k], v, v * 0.1, users, adj_list, used)
            if len(clique) > 3:
                print verbose_list(clique)
            for (k, v) in build_used.iteritems():
                used[k] = v

def analyse2(self_id, min_threshold, adj_list):
    global g_used
    my_friends = sorted(adj_list[self_id].items(), key=lambda x: -x[1])
    used = {}

    for (k, v) in my_friends:
        if k not in g_used:
            clique, build_used = build_clique2(self_id, min_threshold, adj_list, g_used)
            if len(clique) > 3:
                print verbose_list(clique)
            g_used.update(build_used)

def build_clique2(self_id, min_threshold, adj_list, used):
    my_friends = sorted(adj_list[self_id].items(), key=lambda x: -x[1])
    clique = [self_id]

    # Try to add people into the clique (in desc order)
    for (k, v) in my_friends:
        cur_id = k
        add = True
        for user in clique:
            link_str = adj_list[user][cur_id]
            if link_str < min_threshold:
                add = False
        if add:
            if cur_id not in used.keys():
                used[cur_id] = 1
                clique.append(cur_id)

    # print verbose_list(clique)
    return clique, used


if __name__ == '__main__':
    self_id = "601910818"
    # combine(self_id)
    adj_list, users = load_data("mark_data.p")
    g_users = users
    # analyse(self_id, users, adj_list)
    for i in range(40, 0, -2):
        analyse2(self_id, i, adj_list)
    # print adj_list
