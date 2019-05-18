# -*- coding: utf-8 -*

import json
from collections import defaultdict
from pprint import pprint

filter_file = "/home/ubuntu/lichengzhi/HRL-RE/data/person/person.data.json"


def load_filter(filter_file):
    with open(filter_file, "r") as f:
        line = f.readline()
        ret = defaultdict(list)
        while line:
            data = json.loads(line).get('data')
            if data.get('property'):
                id = data.get('_id')
                key = data.get('_key')
                orgs = data.get('org')
                org = orgs.split(';；')
                per = data.get('per')
                title = data.get('property').get('title')
                if title is None:
                    title = ""
                ret[per].append({
                    "_id": id,
                    "_key": key,
                    "orgs": org,
                    "title": title
                })
            line = f.readline()
    return ret


if __name__ == "__main__":
    person_filter = load_filter(filter_file)
    with open("/home/ubuntu/lichengzhi/HRL-RE/data/person/filtered_person.json", "w", encoding='utf-8') as f:
        for person in person_filter:
            for item in person_filter[person]:
                d = item
                org = ";".join(d.get('orgs'))
                d['orgs'] = org
                d['per'] = person
                f.write(json.dumps(d, ensure_ascii=False))
                f.write('\n')







