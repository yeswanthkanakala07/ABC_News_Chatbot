from elasticsearch import Elasticsearch, NotFoundError

es = Elasticsearch("http://localhost:9200")

def search_articles(query, index_name="abc-news", size=3):
    try:
        response = es.search(
            index=index_name,
            body={
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["Title", "description", "spell", "LeadInText"]
                    }
                }
            },
            size=size
        )
    except NotFoundError:
        print(f"Index '{index_name}' not found.")
        return []
    except Exception as e:
        print(f"Elasticsearch error: {e}")
        return []

    hits = response.get('hits', {}).get('hits', [])
    results = []

    for hit in hits:
        source = hit.get('_source', {})
        article = {
            "title": source.get("Title", ""),
            "description": source.get("description", ""),
            "lead_in": source.get("LeadInText", ""),
            "spell": " ".join(source.get("spell", []) or []),
            "url": source.get("url", "")
        }
        results.append(article)
    return results
