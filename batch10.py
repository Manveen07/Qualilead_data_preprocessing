import pandas as pd

df = pd.read_csv("enriched_with_linkedin.csv")

# Initialize column if not present
if "linkedin_enriched" not in df.columns:
    df["linkedin_enriched"] = False

# Select the next 10 unprocessed leads with a LinkedIn URL
batch = df[(df["linkedin_enriched"] == False) & (df["linkedin_url"].notna())].head(10)

batch.to_csv("batch_to_enrich.csv", index=False)
print("✅ Saved 10 leads to batch_to_enrich.csv")
