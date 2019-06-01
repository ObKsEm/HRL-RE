import json
import os
import random
from collections import defaultdict

if __name__ == '__main__':
    vector = defaultdict(list)
    with open('/home/lichengzhi/HRL-RE/data/person/Tencent_AILab_ChineseEmbedding.txt', 'r') as f:
        line = f.readline()
        items = line.split()
        dim = int(items[1])
        line = f.readline()
        while line:
            items = line.split(' ')
            word = items[0]
            vec = [float(each) for each in items[1:]]
            vector[word] = vec
            line = f.readline()


    dic = set()
    with open('/home/lichengzhi/HRL-RE/data/person/train.json', 'r') as f:
        line = f.readline()
        while line:
            item = json.loads(line)
            words = item.get('sentext').split()
            for word in words:
                dic.add(word)
            line = f.readline()

    with open('/home/lichengzhi/HRL-RE/data/person/vector.txt', 'w') as f:
        for word in dic:
            f.write(word)
            if word in vector.keys():
                for v in vector[word]:
                    f.write(' %.6f' % v)
            else:
                for v in range(dim):
                    f.write(' %.6f' % random.uniform(-1, 1))
            f.write('\n')

