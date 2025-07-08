import csv
from urllib.parse import urlparse, urlunparse


# 🚿 1. Clean query strings from URLs
def strip_tracking_params(url):
    try:
        parsed = urlparse(url)
        cleaned = parsed._replace(query="", fragment="")
        return urlunparse(cleaned)
    except:
        return url
    


input_file = "producthunt_resolved.csv"
output_file = "producthunt_cleaned.csv"

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", newline='', encoding="utf-8") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ["cleaned_url"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        raw_url = row.get("resolved_url", "").strip()

        cleaned_url = strip_tracking_params(raw_url)

        row["cleaned_url"] = cleaned_url

        writer.writerow(row)
        print(f"✅ {raw_url} → {cleaned_url} ({row.get('real_domain',"")})")