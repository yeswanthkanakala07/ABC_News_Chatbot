import boto3
import json 
import os
def load_articles_from_s3(bucket_name, prefix=""):
    s3 = boto3.client('s3', aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"))
    


    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    articles = []
    for obj in response.get("Contents", []):
        key = obj["Key"]
        if key.endswith(".json") or key.endswith(".txt"):
            file = s3.get_object(Bucket=bucket_name, Key=key)
            content = file["Body"].read().decode("utf-8")
            try:
                article = json.loads(content) if key.endswith(".json") else {"title": key, "content": content}
                articles.append(article)
            except Exception as e:
                print(f"❌ Failed to parse {key}: {e}")
    return articles