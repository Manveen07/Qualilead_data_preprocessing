import pandas as pd

# Load main file and enriched batch
df_main = pd.read_csv("enriched_with_linkedin.csv")
df_batch = pd.read_csv("batch_enriched.csv")

# Loop through enriched batch and update main file
for _, row in df_batch.iterrows():
    match = df_main["linkedin_url"] == row["linkedin_url"]
    df_main.loc[match, "linkedin_followers"] = row.get("linkedin_followers", "")
    df_main.loc[match, "industry"] = row.get("industry", "")
    df_main.loc[match, "employee_count"] = row.get("employee_count", "")
    df_main.loc[match, "hq"] = row.get("hq", "")
    df_main.loc[match, "linkedin_enriched"] = True

# Save it back
df_main.to_csv("enriched_with_linkedin.csv", index=False)
print("✅ Main file updated with enriched info and marked as processed.")
print("✅ Saved updated main file to enriched_with_linkedin.csv")