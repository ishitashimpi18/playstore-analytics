-- ============================================================
-- Google Play Store Data Cleaning
-- Goal: turn raw_apps (as scraped) into a clean, analysis-ready table
-- ============================================================

-- Drop the known malformed row: a shifted-column bug where a rating
-- value ("1.9") bled into the Category field during scraping.
DELETE FROM raw_apps
WHERE App = 'Life Made WI-Fi Touchscreen Photo Frame'
  AND Category = '1.9';

-- Build the clean table with proper types.
DROP TABLE IF EXISTS apps_clean;

CREATE TABLE apps_clean AS
SELECT
    App,
    Category,
    Rating,                                              -- ~1,474 NULLs = unrated apps, kept as NULL not 0
    CAST(Reviews AS INTEGER) AS Reviews,
    CAST(REPLACE(REPLACE(Installs, ',', ''), '+', '') AS INTEGER) AS Installs,
    Type,
    CAST(REPLACE(Price, '$', '') AS REAL) AS Price,
    "Content Rating" AS ContentRating,
    Genres,
    "Last Updated" AS LastUpdatedRaw
FROM raw_apps;

-- Deduplicate: dataset was scraped at different times, so some apps
-- repeat. Keep the row with the highest review count per app name.
DROP TABLE IF EXISTS apps_final;

CREATE TABLE apps_final AS
SELECT a.*
FROM apps_clean a
INNER JOIN (
    SELECT App, MAX(Reviews) AS max_reviews
    FROM apps_clean
    GROUP BY App
) b ON a.App = b.App AND a.Reviews = b.max_reviews;
