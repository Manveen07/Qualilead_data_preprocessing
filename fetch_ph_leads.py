import requests
import csv
import os

ACCESS_TOKEN = 'GP8apsXTdNnxqgxKDlK9NMGBZ5tL0pgIGqDDYzIJ1ug'
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# GraphQL query to get latest posts
query = """
{
  posts(order: VOTES,postedAfter: "2025-06-29T00:00:00Z", first: 50) {
    edges {
      node {
        name
        tagline
        website
        createdAt
        votesCount
        reviewsCount
        thumbnail { url }
        topics {
          edges {
            node {
              name
            }
          }
        }
      }
    }
  }
}

"""

# Send POST request to Product Hunt GraphQL API
response = requests.post(
    "https://api.producthunt.com/v2/api/graphql",
    headers=headers,
    json={'query': query}
)

data = response.json()
products = data['data']['posts']['edges']

def load_existing_domains(csv_path):
    if not os.path.exists(csv_path):
        return set()
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return set(row["domain"].strip().lower() for row in reader)
    
# Load existing domains to avoid duplicates
csv_path = "producthunt_leads1.csv"
existing_domains = load_existing_domains(csv_path)
# Parse data
rows = []
for p in products:
    node = p['node']
    name = node['name']
    website = node.get('website', '')
    domain = website.replace("https://", "").replace("http://", "").strip("/") if website else ""
    tags = [t['node']['name'] for t in node['topics']['edges']]
    rows.append({
        "company_name": name,
        "tagline": node.get("tagline", ""),
        "domain": domain,
        "website": website,
        "created_at": node.get("createdAt", ""),
        "votes_count": node.get("votesCount", 0),
        "reviews_count": node.get("reviewsCount", 0),
        "thumbnail": node.get("thumbnail", {}).get("url", ""),
        "tags": ", ".join(tags)
    })
new_rows = [row for row in rows if row["domain"].lower() not in existing_domains]
# Save to CSV
write_mode = "a" if os.path.exists(csv_path) else "w"

# with open(csv_path, write_mode, newline='', encoding='utf-8') as f:
#     writer = csv.DictWriter(f, fieldnames=new_rows[0].keys())
#     writer.writeheader()
#     writer.writerows(new_rows)

# print(f"✅ Saved {len(new_rows)} leads to producthunt_leads.csv")


# Append new rows to CSV
if new_rows:
    write_mode = "a" if os.path.exists(csv_path) else "w"
    with open(csv_path, write_mode, newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=new_rows[0].keys())
        if write_mode == "w":
            writer.writeheader()
        writer.writerows(new_rows)
    print(f"✅ Added {len(new_rows)} new leads to {csv_path}")
else:
    print("🔁 No new leads to add. All domains already exist.")