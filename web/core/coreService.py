'''
Author: Rain 1254895072@qq.com
Date: 2022-10-10 12:36:59
LastEditors: Rain 1254895072@qq,com
LastEditTime: 2022-11-16 15:47:38
FilePath: \E-Commerce_Application-main\data_process.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import csv
from time import time
import jieba.posseg
import pandas as pd
import time


words_data_file = "D:/大三/电子商务应用/exp4/Backend_API/web/words-dict/words.txt"


# 读取代码
def code_conversion(raw_path, csv_path):
    # 生成数据路径
    csv_file = open(csv_path, 'w',encoding="utf-8")
    writer = csv.writer(csv_file)
    writer.writerow(['ID', 'Age', 'Gender', 'Education', 'QueryList'])
    # 转换成utf-8编码的格式
    with open(raw_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        for line in lines[0:-1]:
            # noinspection PyBroadException
            try:
                line.strip()
                data = line.split("\t")
                write_data = [data[0], data[1], data[2], data[3]]
                query_str = ''
                # 去掉最后一个词的结尾分隔符
                data[-1] = data[-1][:-1]
                # 处理query string，并且拼接成一个长字符串
                for d in data[4:]:
                    # noinspection PyBroadException
                    try:
                        cur_str = d.encode('utf-8')
                        cur_str = cur_str.decode('utf-8')
                        query_str += cur_str + '\t'
                    except:
                        continue
                query_str = query_str[:-1]
                write_data.append(query_str)
                writer.writerow(write_data)
            except:
                continue
    csv_file.close()


# 分词代码
def cut_word(csv_path, cut_path):
    df = pd.read_csv(csv_path,engine='python',encoding="utf-8",encoding_errors="ignore")
    query_list = list(df.QueryList)
    csv_file = open(cut_path, 'w',encoding="utf-8")
    POS = {}
    list_len = len(query_list)
    for i in range(list_len):
        for item in query_list[i].split('\t'):
            s = []
            string = ""
            words = jieba.posseg.cut(item)
            # 带有词性的精确分词模式
            allowPOS = ['n', 'v', 'j']
            for word, flag in words:
                POS[flag] = POS.get(flag, 0) + 1
                if (flag[0] in allowPOS) and len(word) >= 2:
                    string += word + ' '
            cur_str = string.encode('utf-8')
            cur_str = cur_str.decode('utf-8')
            if len(string) > 0 and len(string.split(' '))>2:
                s.append(cur_str)
                csv_file.write(' '.join(s)+'\n')
    #         # refresh_output(_visualize(i + 1, list_len))
    print("finished!")
    csv_file.close()


def filterAkey(arr,data_path):
    a= []
    s = arr
    # 生成数据路径
    csv_file = open('./midKey.txt', 'w',encoding="utf-8")
    with open(data_path, 'r', encoding='utf-8',errors="ignore") as file:
        lines = file.readlines()  
        key = []    
        value = []
        for index in range(len(s)):
            key.clear()
            value.clear()
            a.append({})
            for line in lines:
                # print(line)
                str = line.split(' ')
                if s[index] in str:
                    for word in str:
                        if word in a[index] and word != s[index] and word != '\n' :
                            a[index][word] = a[index][word]+1
                        else:
                            a[index][word] = 1
            a[index] = sorted(a[index].items(),key=lambda d: d[1],reverse=True)
            print("%s 的中介关键词为 :"%(s[index]))
            csv_file.write("%s 的中介关键词为 :"%(s[index])+'\n')
            for i in range(25):
                print(a[index][i])
                csv_file.write("%s,%d"%(a[index][i][0],a[index][i][1])+'\n')
    csv_file.close()  


def findcompkey(midkeys,key,data_path):
    with open(data_path, 'r', encoding='utf-8',errors="ignore") as file:
        lines = file.readlines() 
        a = {} 
        for index in range(len(midkeys)):
            for line in lines:
                # print(line)
                str = line.split(' ')
                if midkeys[index] in str:
                    for word in str:
                        if word in a and word != midkeys[index] and word != key and word != '\n' :
                            a[word] = a[word]+1
                        elif word in a and word != '\n':
                            a[word] = a[word] + 1
                        elif word != '\n':
                            a[word] = 1
        a = sorted(a.items(),key=lambda d: d[1],reverse=True)
        for i in range(25):
            print(a[i])


def analyse_inter(keyword, mydb, length):
    inters = mydb.inters
    result = inters.find_one({'keyword':keyword})
    if result is not None:
        x = result
        del x['_id']
        return x
    else:
        a = {}
        keyword_count = 0
        with open(words_data_file, 'r', encoding='utf-8', errors="ignore") as file:
            lines = file.readlines()[0:length]
            for line in lines:
                # print(line)
                strs = line.split(' ')
                if keyword in line:
                    keyword_count +=1
                    for word in strs:
                        if word in a and keyword!= word and word != '\n' :
                            a[word] = a[word]+1
                        elif word not in a and keyword != word and word != '\n':
                            a[word] = 1
        a["count"] = keyword_count
        for k , v in list(a.items()):
            if isinstance(v,str):
                continue
            if v < 10:
                a.pop(k)
        a = sorted(a.items(),key=lambda d: d[1],reverse=True)
        a.insert(1,('keyword',keyword))
        x = inters.insert_one(dict(a))
        return dict(a)

# def inter_word_count(words,mydb,length):
#     dblist = mydb.list_collection_names()
#     with open("./words.txt", 'r', encoding='utf-8',errors="ignore") as file:
#         lines = file.readlines()[0:length]
#         count = {}
#         left_words = []
#         for word in words:
#             if word+"_count" in dblist:
#                 x = mydb[word+"_count"].find_one()
#                 del x["_id"]
#                 count[word] = x[word]
#             else:
#                 count[word] = 0
#                 left_words.append(word)
#         for line in lines:
#             for word in left_words:
#                 if word in line:
#                     count[word] +=1
#         for word in left_words:
#             mydb[word+"_count"].insert_one(dict([(word,count[word])]))
#         return count


def analyse_compkey(keyword, mydb, length=9472411):
    compkeys = mydb.compkeys
    result = compkeys.find_one({"keyword":keyword})
    dict_res = {}
    if result is not None:
        whole_count = result['whole_count']
        result['whole_count']=whole_count+1
        issuccess = compkeys.update_one({'keyword':keyword},{'$set':result})
        del result['_id']
        del result['keyword']
        del result['whole_average']
        del result['whole_count']
        for k, v in list(result.items()):
            dict_res[k] = result[k]['result']
        a = sorted(dict_res.items(), key=lambda d: d[1], reverse=True)
        a = dict(a[:10])
        return a
    inters = analyse_inter(keyword, mydb, length)
    keyword_count = inters["count"]
    inters_words = {}  #用于存放中介关键词的权重
    compkey_words = []
    inter_word = list(inters.keys())[1:12]
    # inters_count = inter_word_count(inter_word,mydb,length)
    for k, v in list(inters.items())[1:12]:
        if k != "_id" and k != "count" and k != 'keyword':
            inters_words[k] = v/keyword_count
            comp = analyse_inter(k,mydb,length)
            inters_count = comp["count"]
            del comp['keyword']
            if keyword in comp:
                del comp[keyword]
            for key, value in list(comp.items()):
                comp[key] = (value/(inters_count-inters[k])) * inters_words[k]
            del comp['count']
            compkey_words.append(comp)
        if len(inters_words) == 10:
            break
    compkey = {}
    for i in compkey_words:
        compkey = sum_dict(compkey,i)
    a = sorted(compkey.items(),key=lambda d: d[1],reverse=True)
    a = dict(a)
    res = {'keyword':keyword,'whole_average':0.5,'whole_count':1}
    for k,v in list(a.items()):
        res[k] = {'competitive': v, 'average': 0.5, 'result': (v * 0.5), 'count': 1}
    x = compkeys.insert_one(res)
    del res['_id']
    del res['keyword']
    del res['whole_average']
    del res['whole_count']
    for k, v in list(res.items()):
        dict_res[k] = res[k]['result']
    a = sorted(dict_res.items(), key=lambda d: d[1], reverse=True)
    a = dict(a[:10])
    return a


def sum_dict(a, b):
    temp = dict()
    # dict_keys类似set； | 并集
    for key in a.keys() | b.keys():
        temp[key] = sum([d.get(key, 0) for d in (a, b)])
    return temp


def premise():
    with open('process_data.txt', 'w', encoding='utf-8') as file:
        print("清空processed_data文件内容")
        # file.write('')

    txt = open('data.txt', 'r', encoding='utf-8',errors="ignore")
    num = 1
    while True:
        line = txt.readline().strip()
        if not line:
            break
        search_info = line.split('\t')[4:]
        search_info = ' '.join(search_info)
        search_info = search_info.split(' ')
        for search in search_info:
            with open('process_data.txt', 'a', encoding='utf-8') as file1:
                print(num, ":", search)
                num += 1
                file1.write(search + '\n')


def update_compkey(mydb, keyword, compkey, score: float):
    compkeys = mydb.compkeys
    result = compkeys.find_one({"keyword":keyword})
    old_score = result[compkey]['average']
    if old_score - score < 0.3 and score - old_score < 0.3:
        for k , v  in list(result.items()):
            if isinstance(v,dict):
                if v['count'] ==1:
                    v['average'] = result['whole_average']
                    v['result'] = v['average'] * v['competitive']
        data = result[compkey]
        data['count'] = data['count']+1
        data['average'] = (data['average'] * (data['count']-1) + float(score)) / data['count']
        data['result'] = data['average'] * data['competitive']
        result[compkey] = data
        whole_count = result['whole_count']
        whole_average = result['whole_average']
        # result['whole_count'] = whole_count + 1
        result['whole_average'] = (whole_average * (whole_count)+float(score))/(whole_count+1)
    
        issuccess = compkeys.update_one({'keyword': keyword}, {'$set': result})
        print(issuccess)
        return issuccess


def get_access_count(mydb):
    # 返回用户搜索次数和rank10的搜索keyword和对应的搜索次数
    # return count 
    # return dict: {"a":10,'b'}
    compkeys = mydb.compkeys
    result = compkeys.find()
    count = 0
    dict_count = {}
    for i in result:
        count = count + i['whole_count']
        dict_count[i['keyword']] = i['whole_count']
    a = sorted(dict_count.items(),key=lambda d: d[1],reverse=True)
    if len(a) > 10:
        a = dict(a[:10])
    else:
        a = dict(a)
    return count, a


def get_compkeys(mydb):
    #返回所有查询过的词和相应的信息
    compkeys = mydb.compkeys
    result = compkeys.find()
    dict_word = {}
    for i in result:
        temp = {}
        temp['whole_average'] = i['whole_average']
        temp['whole_count'] = i['whole_count']
        dict_word[i['keyword']] = temp
    return dict_word


def get_comkeys_details(mydb, keyword):
    # 返回keyword的全部竞争性关键词（排好序的，按计算过的竞争度）
    compkeys = mydb.compkeys
    result = compkeys.find_one({"keyword":keyword})
    del result['_id']
    del result['keyword']
    del result['whole_average']
    del result['whole_count']
    dict_res = {}
    result = sorted(result.items(),key=lambda item:item[1]['competitive'],reverse=True)
    return dict(result)

