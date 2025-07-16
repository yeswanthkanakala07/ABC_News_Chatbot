from elasticsearch import Elasticsearch
import uuid
import re

es = Elasticsearch("http://localhost:9200")  # Or your ES endpoint

def fix_date_format(date_str):
    if isinstance(date_str, str):
        return re.sub(r'(\d{2}):(\d{3}-\d{2})$', r'.\2', date_str)
    return date_str

def clean_article(article):
    if "_source" in article:
        article = article["_source"]
    for date_field in ["lastPublishedDate", "createDate"]:
        if date_field in article:
            article[date_field] = fix_date_format(article[date_field])
    return article

def _index_single_article(article, index_name):
    article = clean_article(article)
    doc_id = str(article.get("id") or article.get("_id") or uuid.uuid4())
    es.index(index=index_name, id=doc_id, document=article)

def index_articles(articles, index_name="abc-news"):
    for article in articles:
        if isinstance(article, list):
            for sub_article in article:
                if isinstance(sub_article, dict):
                    _index_single_article(sub_article, index_name)
        elif isinstance(article, dict):
            _index_single_article(article, index_name)