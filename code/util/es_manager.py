# -*- coding: utf-8 -*-
import hashlib

from elasticsearch import Elasticsearch, NotFoundError

ES_HOST = '39.107.88.169'
ES_PORT = '59200'

INDEX_SOURCE = [
    "wechat_ner",
    "toutiao_ner",
    "manual_ner",
    "baidu_ner",
    "36kr_ner"
]

DOC_TYPE = 'items'
DOC_TYPE_NEWS = 'news'



ES_MAPPINGS = {
    'es_ids': (INDEX_SOURCE_POINTS, DOC_TYPE),
    INDEX_SOURCE_POINTS: (INDEX_SOURCE_POINTS, DOC_TYPE),
    INDEX_WECHAT: (INDEX_WECHAT, DOC_TYPE_NEWS),
    INDEX_TOUTIAO: (INDEX_TOUTIAO, DOC_TYPE_NEWS),
    INDEX_36KR: (INDEX_36KR, DOC_TYPE_NEWS),
    INDEX_BAIDU: (INDEX_BAIDU, DOC_TYPE_NEWS),
}


def connect(host=ES_HOST, port=ES_PORT):
    return Elasticsearch(host, port=port)


def connect_by_index(index):
    if INDEX_SOURCE_POINTS == index:
        return connect()
    return connect(ES_HOST_SEARCHER, ES_PORT_SEARCHER)


def get_es_query_by_engine(engine):
    return {
        "query": {
            "bool": {
                "filter": [
                    {"term": {"engine": engine}}
                ]
            }
        },
        "size": 0
    }


def get_by_id(client, _id, index=INDEX_SOURCE_POINTS, doc_type=DOC_TYPE):
    try:
        return client.get(index=index, doc_type=doc_type, id=_id)
    except NotFoundError:
        return None


def get_by_ids(client, id_list, index=INDEX_SOURCE_POINTS, doc_type=DOC_TYPE):
    try:
        return client.mget(index=index, doc_type=doc_type, body={"ids": id_list})
    except NotFoundError:
        return None


def search(client, query, index=INDEX_SOURCE_POINTS, size=50, scroll=None, timeout='30s', request_timeout=30):
    if query is None or len(query) == 0:
        return None

    if scroll is None or len(scroll) == 0:
        data = client.search(
            index=index,
            size=size,
            body=query,
            timeout=timeout,
            request_timeout=request_timeout
        )
        hits = data['hits']['hits']
        for hit in hits:
            yield hit

    else:
        data = client.search(
            index=index,
            scroll=scroll,
            size=size,
            body=query,
            timeout=timeout,
            request_timeout=request_timeout
        )
        hits = data['hits']['hits']
        for hit in hits:
            yield hit

        sid = data['_scroll_id']
        scroll_size = len(data['hits']['hits'])
        while scroll_size > 0:
            data = client.scroll(scroll_id=sid, scroll=scroll)

            hits = data['hits']['hits']
            for hit in hits:
                yield hit

            sid = data['_scroll_id']
            scroll_size = len(data['hits']['hits'])


def delete_by_id(client, _id):
    client.delete(index=INDEX_SOURCE_POINTS, doc_type=DOC_TYPE, id=_id)


def get_total_by_engine(engine):
    data = connect().search(
        index=INDEX_SOURCE_POINTS,
        size=0,
        body=get_es_query_by_engine(engine)
    )
    return data['hits']['total']


def update(client, _id, doc=None, script=None, index=INDEX_SOURCE_POINTS, doc_type=DOC_TYPE):
    if doc:
        client.update(index, doc_type=doc_type, id=_id, body={'doc': doc})
    elif script:
        client.update(index, doc_type=doc_type, id=_id, body={'script': script})


def gen_id_by_url(url):
    if url is None:
        return None
    unique_key = url.encode('utf-8')
    return hashlib.sha1(unique_key).hexdigest()
