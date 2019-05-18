import json
from collections import defaultdict
from elasticsearch import Elasticsearch

from util import baidu

INDEX_SOURCE = [
    "wechat_ner",
    "toutiao_ner",
    "manual_ner",
    "baidu_ner",
    "36kr_ner"
]

NER_ITEM = ['ORG', 'PER', 'LOC']


def check_filter(filter_dict, per, org, title):
    if filter_dict.get(per) is not None:
        for item in filter_dict[per]:
            filter_orgs = item.get('orgs')
            filter_title = item.get('title')
            # print('item: ')
            # print(item)
            # print(filter_orgs)
            # print(filter_title)
            if (filter_orgs.find(org) > -1) and (filter_title.find(title) > -1):
                return True
    return False


def get_data_from_es(filter_dict):
    es_data_size = 0
    query = {
        "query": {
            "match_all": {}
        }
    }
    client = Elasticsearch("http://39.96.12.237", port=59200)
    data = client.search(
        index=INDEX_SOURCE,
        scroll='5m',
        size=100,
        timeout='3s',
        body=query
    )
    num = 0
    hits = data['hits']['hits']
    res = list()
    for hit in hits:
        index = hit.get('_index')
        es_id = hit.get('_id')
        rel = hit.get('_source').get('rel')
        if rel:
            for each in rel:
                each['_index'] = index
                each['_id'] = es_id
                per = each.get('per')
                org = each.get('org')
                title = each.get('title')
                sentext_list = each.get('relateto')
                # sentence = ''.join(sentext_list)
                for sentence in sentext_list:
                    if check_filter(filter_dict, per, org, title):
                        res.append({
                                "sentence": sentence,
                                "entities": [per, org],
                                "ID": num,
                                "relations": {
                                    "rtext": title,
                                    "em2": org,
                                    "em1": per,
                                }
                            })
                        num += 1
    scroll_id = data["_scroll_id"]
    scroll_size = len(data['hits']['hits'])
    es_data_size += scroll_size
    # scroll_size = 0
    while scroll_size > 0:
        print("processed_es_data_size: %d\n" % (es_data_size))
        data = client.scroll(scroll_id=scroll_id, scroll='5m')  # scroll参数必须指定否则会报错
        hits = data["hits"]["hits"]
        scroll_id = data['_scroll_id']
        for hit in hits:
            index = hit.get('_index')
            es_id = hit.get('_id')
            rel = hit.get('_source').get('rel')
            if rel:
                for each in rel:
                    each['_index'] = index
                    each['_id'] = es_id
                    per = each.get('per')
                    org = each.get('org')
                    title = each.get('title')
                    sentext_list = each.get('relateto')
                    # sentence = ''.join(sentext_list)
                    for sentence in sentext_list:
                        if check_filter(filter_dict, per, org, title):
                            res.append({
                                "_index": index,
                                "_id": es_id,
                                "sentence": sentence,
                                "relations": {
                                    "rtext": title,
                                    "em2": org,
                                    "em1": per,
                                }
                            })
                            num += 1
        scroll_size = len(data['hits']['hits'])
        es_data_size += scroll_size
    return res


if __name__ == "__main__":
    # data_file = "/home/ubuntu/lichengzhi/HRL-RE/data/person/filtered_person.json"
    data_file = "/Users/lichengzhi/bailian/HRL-RE/data/person/filtered_person.json"
    filter_dict = defaultdict(list)
    with open(data_file, "r", encoding='utf-8') as f:
        line = f.readline()
        while line:
            item = json.loads(line)
            person = item.get('per')
            d = dict()
            for key in item:
                if key != "per":
                    d[key] = item[key]
            filter_dict[person].append(d)
            line = f.readline()

    row_data = get_data_from_es(filter_dict)
    with open('row_data.json', 'w', encoding='utf-8') as f:
        for item in row_data:
            f.write(json.dumps(item, ensure_ascii=False))
            f.write('\n')

    with open('train.json', 'w', encoding='utf-8') as f:
        num = 0
        for item in row_data:
            find_em1 = False
            find_em2 = False
            repeat_entity = False
            sentence = item.get('sentence').replace(' ', '')
            pos = baidu.original_lexer(sentence)
            if pos is not None:
                words = [pos[i].get('item') for i in range(0, len(pos))]
                sentext = " ".join(words)
                tags = list()
                entities = set()
                entry = ''
                entry_length = 0
                em1 = item.get('relations').get('em1')
                em2 = item.get('relations').get('em2')
                title = item.get('relations').get('rtext')
                for i in range(0, len(pos)):
                    term = pos[i]
                    word = term.get('item')
                    entry = entry + word
                    entry_length += 1
                    if em1.find(entry) >= 0:
                        if em1 == entry:
                            if find_em1:
                                repeat_entity = True
                                break
                            entities.add(entry)
                            tags.append(4)
                            tags.extend([1] * (entry_length - 1))
                            entry_length = 0
                            find_em1 = True

                    elif em2.find(entry) >= 0:
                        if em2 == entry:
                            if find_em2:
                                repeat_entity = True
                                break
                            entities.add(entry)
                            tags.append(5)
                            tags.extend([2] * (entry_length - 1))
                            entry_length = 0
                            find_em2 = True
                    else:
                        entry = ''
                        for history in range(i - entry_length + 1, i + 1):
                            if pos[history].get('ne') in NER_ITEM:
                                tags.append(6)
                                entities.add(pos[history].get('item'))
                            else:
                                tags.append(0)
                        entry_length = 0
                if (find_em1) and (find_em2) and (not repeat_entity):
                    num += 1
                    res = {
                        'sentence': sentence,
                        'sentext': sentext,
                        'entities': list(entities),
                        'ID': num,
                        'relations': [
                            {
                                'rtext': title,
                                'em2': em2,
                                'em1': em1,
                                'tags': tags
                            }
                        ]
                    }
                    if num % 10000 == 0:
                        print("Saving data: %d\n" % num)
                    f.write(json.dumps(res, ensure_ascii=False))
                    f.write('\n')








