#!/usr/bin/env python3
"""Post blog articles to LinkedIn."""
import os, json, urllib.request
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("LINKEDIN_ACCESS_TOKEN")
if not token:
    print("No LinkedIn access token found")
    exit(1)

# Get person URN
req = urllib.request.Request("https://api.linkedin.com/v2/userinfo", headers={"Authorization": f"Bearer {token}"})
resp = urllib.request.urlopen(req, timeout=15)
profile = json.loads(resp.read())
person_urn = profile["sub"]
name = f"{profile.get('given_name', '')} {profile.get('family_name', '')}"
print(f"Connected as: {name} (URN: {person_urn})")

POST_URL = "https://victor-kipruto-rop.github.io/victor-resum-web/post/?id="
BLOG_URL = "https://victor-kipruto-rop.github.io/victor-resum-web/blog/"

posts = [
    ("Building a Modern Data Lakehouse: From Architecture to Implementation", "data-lakehouse-architecture-from-architecture-to-implementation", ["DataLakehouse", "DeltaLake", "ApacheSpark", "DataEngineering"]),
    ("Mastering Apache Spark Shuffle Operations", "mastering-apache-spark-shuffle-operations-for-large-scale-data-processing", ["ApacheSpark", "BigData", "Performance", "DataEngineering"]),
    ("Optimizing Snowflake Virtual Warehouses for Cost and Performance", "optimizing-snowflake-virtual-warehouses-for-cost-and-performance", ["Snowflake", "CostOptimization", "Cloud", "DataEngineering"]),
    ("Production-Grade Python Testing Strategies for Data Pipelines", "production-grade-python-testing-strategies-for-data-pipelines", ["Python", "Testing", "DataPipelines", "CICD"]),
    ("Building a Real-Time Dashboard Pipeline with Flink, Kafka, and Grafana", "building-a-real-time-dashboard-pipeline-with-flink-kafka-and-grafana", ["Flink", "Kafka", "Grafana", "RealTime"]),
]

success = 0
for title, post_id, tags in posts:
    url = POST_URL + post_id
    tag_str = " ".join([f"#{t}" for t in tags])
    text = f"📝 New Blog Post: {title}\n\nI just published a new technical deep-dive covering practical patterns and real-world code examples.\n\nRead the full article: {url}\n\n{tag_str}"

    post_data = {
        "author": f"urn:li:person:{person_urn}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text},
                "shareMediaCategory": "ARTICLE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }

    try:
        data = json.dumps(post_data).encode()
        req = urllib.request.Request("https://api.linkedin.com/v2/ugcPosts", data=data, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json", "X-Restli-Protocol-Version": "2.0.0"})
        resp = urllib.request.urlopen(req, timeout=15)
        result = json.loads(resp.read())
        print(f"✓ Posted: {title[:50]}... (ID: {result.get('id', 'N/A')[:20]})")
        success += 1
    except Exception as e:
        print(f"✗ Failed: {title[:50]}... ({str(e)[:60]})")

print(f"\nResult: {success}/{len(posts)} posts published to LinkedIn")