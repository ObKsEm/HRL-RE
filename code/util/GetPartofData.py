import json
import random

train_data_size = 100000
test_data_size = 5000

if __name__ == '__main__':
    train_data = list()
    test_data = list()
    relations = set()

    with open('/home/lichengzhi/HRL-RE/data/person/whole_data/train.json', 'r') as f:
        num = 0
        line = f.readline()
        while line and num < train_data_size:
            rd = random.uniform(0, 1)
            if 0 <= rd <= 0.5:
                num += 1
                item = json.loads(line)
                for rel in item.get('relations'):
                    relations.add(rel.get('rtext'))
                train_data.append(item)

            line = f.readline()
        pass
        num = 0
        while line and num < test_data_size:
            rd = random.uniform(0, 1)
            if 0 <= rd <= 0.3:
                num += 1
                item = json.loads(line)
                inset = True
                for rel in item.get('relations'):
                    if rel.get('rtext') not in relations:
                        inset = False
                        break
                if inset:
                    test_data.append(json.loads(line))
            line = f.readline()

    with open('/home/lichengzhi/HRL-RE/data/person/train.json', 'w', encoding='utf-8') as f:
        for line in train_data:
            f.write(json.dumps(line, ensure_ascii=False))
            f.write('\n')

    with open('/home/lichengzhi/HRL-RE/data/person/test.json', 'w', encoding='utf-8') as f:
        for line in test_data:
            f.write(json.dumps(line, ensure_ascii=False))
            f.write('\n')

