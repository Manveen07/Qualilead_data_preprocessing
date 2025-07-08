import csv
import dns.resolver

# Generate common email guesses for a given domain
def guess_email(domain):
    prefixes = ["contact", "info", "hello", "team", "support"]
    return [f"{prefix}@{domain}" for prefix in prefixes]

# Check if domain has MX records (i.e., can receive emails)
def has_mx_record(domain):
    try:
        dns.resolver.resolve(domain, "MX")
        return True
    except:
        return False

# Load leads and enrich with email
enriched_rows = []
with open("producthunt_cleaned.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        domain = row["real_domain"].strip().lower()
        print(f"🔍 Processing domain: {domain}")
        guessed_emails = guess_email(domain)
    
        valid_email = ""
        for email in guessed_emails:
            email_domain = email.split("@")[1]
            if has_mx_record(email_domain):
                print(f"✅ Valid email guess: {email} for domain: {domain}")
                valid_email = email
                break

        row["email_guess"] = valid_email
        row["email_valid"] = True if valid_email else False
        enriched_rows.append(row)

# Save enriched leads
with open("enriched_leads.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=enriched_rows[0].keys())
    writer.writeheader()
    writer.writerows(enriched_rows)

print(f"✅ Enriched {len(enriched_rows)} leads with email guesses and validation.")
print(f"✅ Saved enriched leads to enriched_leads.csv")