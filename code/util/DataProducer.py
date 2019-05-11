import json
from collections import defaultdict
from elasticsearch import Elasticsearch


INDEX_SOURCE = [
    "wechat_ner",
    "toutiao_ner",
    "manual_ner",
    "baidu_ner",
    "36kr_ner"
]


def check_filter(filter_dict, per, org, title):
    for item in filter_dict[per]:
        orgs = item.get('orgs')
        title = item.get('title')
        if (orgs.find(org) > -1) and (title.find(title) > -1):
            return True
    return False



def get_data_from_es(filter_dict):
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
                per = rel.get('per')
                org = rel.get('org')
                title = rel.get('title')
                sentext_list = rel.get('relateto')
                # sentence = ''.join(sentext_list)
                for sentence in sentext_list:
                    if check_filter(filter_dict, per, org, title):
                        res.append({
                                "sentext": sentence,
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
    while scroll_size > 0:
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
                res.extend(rel)
        scroll_size = len(data['hits']['hits'])
    return res


if __name__ == "__main__":
    data_file = "../../data/person/fileterd_person.json"
    filter_dict = defaultdict(list)
    with open(data_file, "r", encoding='utf-8') as f:
        line = f.readline()
        while line:
            item = json.loads(line)
            person = item.get('per')
            for key in item:
                d = dict()
                if key != "per":
                    d[key] = item[key]
            filter_dict[person].append(d)
            line = f.readline()
    row_data = get_data_from_es(filter_dict)

