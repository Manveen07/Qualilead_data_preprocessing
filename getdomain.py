# import requests
# from urllib.parse import urlparse
# import csv


# def resolve_redirect(url):
#     try:
#         if not url.startswith("http"):
#             url = "https://" + url  # 🔧 Ensure it's a valid absolute URL
#         res = requests.get(url, allow_redirects=True, timeout=10)
#         return res.url
#     except Exception as e:
#         print(f"⚠️ Redirect failed for {url}: {e}")
#         return ""

# def extract_domain(url):
#     try:
#         parsed = urlparse(url)
#         return parsed.netloc.replace("www.", "")
#     except:
#         return ""

# input_file = "producthunt_leads.csv"
# output_file = "cleaned_leads.csv"

# with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", newline='', encoding="utf-8") as outfile:
#     reader = csv.DictReader(infile)
#     fieldnames = reader.fieldnames + ["resolved_website", "clean_domain"]
#     writer = csv.DictWriter(outfile, fieldnames=fieldnames)
#     writer.writeheader()

#     for row in reader:
#         raw_url = row.get("domain", "") or row.get("website", "")  # fallback
#         resolved_url = resolve_redirect(raw_url)
#         clean_domain = extract_domain(resolved_url)

#         row["resolved_website"] = resolved_url
#         row["clean_domain"] = clean_domain

#         writer.writerow(row)
#         print(f"✅ Processed: {raw_url} → {clean_domain}")

# print(f"\n✅ Done. Cleaned CSV saved to: {output_file}")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from urllib.parse import urlparse
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# 1. Setup headless browser
def create_driver():
    options = Options()
    options.add_argument("--headless=new")  # use the newer headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 2. Follow redirect & extract domain
def resolve_domain(driver, url):
    try:
        if not url.startswith("http"):
            url = "https://" + url
        driver.get(url)
        time.sleep(4)  # give it time to complete JS redirect
        final_url = driver.current_url
        parsed = urlparse(final_url)
        domain = parsed.netloc.replace("www.", "")
        return final_url, domain
    except Exception as e:
        print(f"⚠️ Failed to resolve {url}: {e}")
        return "", ""

# 3. Process CSV
input_file = "producthunt_leads1.csv"
output_file = "producthunt_resolved.csv"

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", newline='', encoding="utf-8") as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ["resolved_url", "real_domain"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    driver = create_driver()

    for row in reader:
        raw_url = row.get("website", "").strip()
        if not raw_url:
            row["resolved_url"] = ""
            row["real_domain"] = ""
            print(f"❌ No URL found for row: {row}")
        else:
            resolved_url, domain = resolve_domain(driver, raw_url)
            row["resolved_url"] = resolved_url
            row["real_domain"] = domain
            print(f"✅ Resolved: {raw_url} → {resolved_url} ({domain})")
        writer.writerow(row)

    driver.quit()

print(f"\n✅ Done. Cleaned CSV saved to: {output_file}")
