import pandas as pd
import sqlite3
import urllib.request

# --- Load raw data ---
url = "https://raw.githubusercontent.com/sumitgirwal/google-play-store-data-analysis/master/googleplaystore.csv"
urllib.request.urlretrieve(url, "googleplaystore.csv")

df = pd.read_csv("googleplaystore.csv")
conn = sqlite3.connect("playstore.db")
df.to_sql("raw_apps", conn, if_exists="replace", index=False)

# --- Run the cleaning SQL (see 01_clean_data.sql for the same logic) ---
cur = conn.cursor()
with open("01_clean_data.sql", "r") as f:
    cur.executescript(f.read())
conn.commit()

# --- Query 1: Underrated categories (high rating, low installs) ---
q1 = """
SELECT
    Category,
    ROUND(AVG(Rating), 2) AS avg_rating,
    ROUND(AVG(Installs), 0) AS avg_installs,
    COUNT(*) AS num_apps
FROM apps_final
WHERE Rating IS NOT NULL
GROUP BY Category
HAVING num_apps >= 20
ORDER BY avg_rating DESC, avg_installs ASC
LIMIT 10;
"""
df1 = pd.read_sql(q1, conn)

# --- Query 2: Paid vs Free rating comparison by category ---
q2 = """
SELECT
    Category,
    Type,
    ROUND(AVG(Rating), 2) AS avg_rating,
    ROUND(AVG(Installs), 0) AS avg_installs,
    COUNT(*) AS num_apps
FROM apps_final
WHERE Rating IS NOT NULL AND Type IN ('Free', 'Paid')
GROUP BY Category, Type
HAVING num_apps >= 5
ORDER BY Category, Type;
"""
df2 = pd.read_sql(q2, conn)

# --- Query 3: Update recency vs rating ---
df_final = pd.read_sql("SELECT * FROM apps_final WHERE Rating IS NOT NULL", conn)
df_final["LastUpdatedYear"] = pd.to_datetime(df_final["LastUpdatedRaw"], errors="coerce").dt.year

q3 = df_final.groupby("LastUpdatedYear").agg(
    avg_rating=("Rating", "mean"),
    num_apps=("App", "count")
).round(2).reset_index()

# --- Export for Google Sheets dashboard ---
df1.to_csv("insight1_underrated_categories.csv", index=False)
df2.to_csv("insight2_paid_vs_free.csv", index=False)
q3.to_csv("insight3_update_recency_vs_rating.csv", index=False)

print("Findings 1 (underrated categories):\n", df1)
print("\nFindings 2 (paid vs free):\n", df2.head(20))
print("\nFindings 3 (update recency):\n", q3)
