from s3_loader import load_articles_from_s3
from es_ingest import index_articles

bucket = "yeshsampledata"
prefix = ""  # Or "articles/" if your files are in a folder

try:
    articles = load_articles_from_s3(bucket, prefix)
    print(f"✅ Loaded {len(articles)} articles")
    if articles:
        index_articles(articles)
        print("✅ Indexed into Elasticsearch")
    else:
        print("⚠️ No articles found to index.")
except Exception as e:
    print(f"❌ Error: {e}")