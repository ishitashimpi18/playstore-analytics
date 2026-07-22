# Google Play Store App Performance Analysis
**Live Dashboard:** [Google Sheets Dashboard](https://docs.google.com/spreadsheets/d/1T60SvwNBoAMWt-PeLT53PGaXkutoLc1jsKrB_YV6Zf4/edit?usp=sharing)

Analysis of ~10,000 Google Play Store apps to identify monetization,
discovery, and maintenance patterns that drive app performance —
built with SQL for cleaning/querying and Google Sheets for visualization.

## Data Source
[Google Play Store Apps dataset](https://www.kaggle.com/lava18/google-play-store-apps) — ~10,840 apps scraped from the Play Store, with category, rating, installs, price, and update-history fields.

## Data Cleaning (SQL)
Raw data required real cleanup before analysis:
- **Fixed a shifted-column bug**: one row had a rating value ("1.9") bled into the Category field due to a scraping error — identified and dropped.
- **Type casting**: `Installs` (e.g. "10,000+") and `Price` (e.g. "$4.99") were stored as text; cast to numeric using `REPLACE()` + `CAST()`.
- **Deduplication**: the dataset was scraped at different points in time, so ~786 apps appeared more than once — kept the entry with the highest review count per app as the most complete snapshot.
- **Handled missing data explicitly**: ~1,472 apps have no rating yet — kept as NULL rather than defaulting to 0, since "unrated" and "rated poorly" are different facts.

See [`01_clean_data.sql`](./01_clean_data.sql) for the full cleaning script.

## Key Findings

**1. Quality and reach don't always move together.**
EVENTS (4.44★ avg) and ART_AND_DESIGN (4.36★ avg) are the highest-rated
categories in the dataset, yet have among the lowest average installs
(354K and 1.9M) — compared to GAME and SOCIAL, which average 17M–28M
installs despite slightly lower ratings (~4.25★). These categories
aren't underperforming on quality; they're underperforming on discovery.

**2. Monetization strategy should be category-specific, not uniform.**
In FAMILY and BUSINESS, paid apps rate higher than free ones (FAMILY:
4.29 vs 4.17; BUSINESS: 4.20 vs 4.11). In FINANCE and COMMUNICATION, it
reverses (FINANCE: 3.83 paid vs 4.13 free) — likely because strong free
incumbents already set the quality bar in those categories.

**3. Active maintenance correlates with better ratings.**
Average rating rose steadily from 3.79 (2012) to 4.23 (2018), the most
recent and highest-rated cohort in the dataset — suggesting update
frequency functions as a retention/quality signal, not just a
maintenance formality.

## Recommendation
A new app team should: (1) invest in ASO/discovery for high-quality,
under-served niches like Events and Art & Design rather than assuming
quality alone drives installs; (2) set pricing based on category norms
rather than a flat strategy; and (3) treat update cadence as a
retention lever worth resourcing, not a low-priority chore.

## Tools
SQL (SQLite), Python (pandas, for CSV export and date parsing),
Google Sheets (dashboard and visualization)
