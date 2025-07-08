import requests
import csv


API_KEY = "RIABWwTL3cx8JjKTkKDl_A"


def enrich_linkedin(linkedin_url):
    url = "https://nubela.co/proxycurl/api/linkedin/company"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {"url": linkedin_url, "use_cache": "if-present"}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed for {linkedin_url}: {response.status_code}")
            return {}
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return {}

input_file = "batch_to_enrich.csv"
output_file = "batch_enriched.csv"

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", newline='', encoding="utf-8") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ["linkedin_followers", "industry", "employee_count", "hq"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        linkedin_url = row.get("linkedin_url", "")
        data = enrich_linkedin(linkedin_url)

        row["linkedin_followers"] = data.get("follower_count", "N/A")
        row["industry"] = data.get("industry", "N/A")
        row["employee_count"] = data.get("employee_count", "N/A")
        row["hq"] = data.get("hq", "N/A")

        print(f"✅ {row['company_name']} → {row['linkedin_followers']} followers")
        writer.writerow(row)

print(f"\n✅ Done. Enriched CSV saved to: {output_file}")