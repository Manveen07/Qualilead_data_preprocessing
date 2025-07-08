import requests
import csv

GOOGLE_API_KEY = "AIzaSyChHsgpa2BcTwsMh2ZdFnViHUTYgtMOS28"
SEARCH_ENGINE_ID = "14c8f42709fc94d89"

def find_linkedin(company_name):
    query = f"site:linkedin.com/company {company_name}"
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}"

    try:
        response = requests.get(url)
        items = response.json().get("items", [])
        for item in items:
            link = item.get("link", "")
            if "linkedin.com/company" in link:
                return link
    except Exception as e:
        print(f"⚠️ Failed LinkedIn search for {company_name}: {e}")
    return ""

# Load and enrich CSV
input_file = "enriched_leads.csv"
output_file = "enriched_with_linkedin.csv"

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", newline='', encoding="utf-8") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ["linkedin_url"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        name = row["company_name"]
        linkedin_url = find_linkedin(name)
        row["linkedin_url"] = linkedin_url
        print(f"✅ {name} → {linkedin_url}")
        writer.writerow(row)

print(f"\n✅ Done. Saved enriched leads with LinkedIn to: {output_file}")
