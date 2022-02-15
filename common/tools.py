'''
Created on 2022-2-11

@author: Administrator
'''
import configparser
import os


def get_fpath(folder, fname):
    path = os.path.abspath("..")
    file_path = os.path.join(path,"%s\\" % folder)
    fpath=os.path.join(file_path,"%s" % fname)
    if os.path.exists(file_path):
        return fpath
    else:
        os.mkdir(file_path)
        return fpath


def get_idkey_dict(data_list):
    """
    :param: data_list=[{"id":1,"a":3,"b":3},{"id":1,"a":4,"b":4},{"id":2,"a":5,"b":5},{"id":2,"a":6,"b":6}]
    :return: {1: [{'b': 3, 'a': 3}, {'b': 4, 'a': 4}], 2: [{'b': 5, 'a': 5}, {'b': 6, 'a': 6}]}
    """
    l = {}
    for data in data_list:
        key = data.pop("id")
        if key in l.keys():
            l[key].append(data)
        else:
            l[key] = [data]
    return l


def get_key_item(list, key):
    """
    :param:list:[{"a":1,"b":2},{"a":3,"b":4}]
    :param:key:"a"
    :return:l:[1, 3]
    """
    l = []
    for d in list:
        if key in d.keys():
            l.append(d.get(key))
        else:
            continue
    return l


def get_conf(section, option=""):
    cfgpath = get_fpath("config", "conf.ini")
    conf = configparser.ConfigParser()
    conf.read(cfgpath, encoding='utf8')
    if option:
        try:
            value = conf.get(section, option)
            return value
        except Exception as e:
            print("section or option is not find,reason:%s" % e)
    else:
        l = {}
        try:
            items = conf.items(section)
            for i in items:
                l[i[0]] = i[1]
        except Exception as e:
            print("section is not find,reason:%s" % e)
        return l




