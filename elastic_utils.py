from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

def search_articles(query, index="abc-news"):
    body = {
        "query": {
            "match": {
                "content": query
            }
        }
    }
    res = es.search(index=index, body=body)
    return [hit["_source"] for hit in res["hits"]["hits"]]