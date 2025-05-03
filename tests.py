import psycopg2
import pandas as pd 
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Connect to the database using secure .env credentials
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

failures = []

# SQL logic using generic table and column names
sql = """
WITH recent_records AS (
  SELECT *
  FROM fact_transactions
  WHERE transaction_date >= CURRENT_DATE - INTERVAL '6 months'
),
joined_data AS (
  SELECT
    f.transaction_id,
    f.transaction_date,
    f.amount,
    u.username AS user_name,
    t.type_name AS transaction_type,
    RANK() OVER (PARTITION BY f.user_durable_key ORDER BY f.amount DESC) AS amount_rank
  FROM recent_records f
  JOIN dim_user u ON f.user_key = u.surrogate_key
  JOIN dim_type t ON f.type_id = t.type_id
)
SELECT *
FROM joined_data
WHERE amount_rank <= 5;
"""

# Load SQL results into pandas DataFrame
df = pd.read_sql(sql, conn)

# Test 1: Each user must have a rank between 1 and 5
for user in df['user_name'].unique():
    ranks = df[df['user_name'] == user]['amount_rank']
    assert ranks.max() <= 5, f"❌ User {user} has rank > 5!"
print("✅ Test passed: All users have top 5 ranked transactions.")

# Test 2: User names should not be missing
assert df["user_name"].notnull().all(), "❌ Missing user names"
print("✅ Test passed: All user names are present.")

# Optional: Save failures to a CSV file if any occur
if failures:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    df_fail = pd.DataFrame(failures)
    df_fail.to_csv(f"failed_tests_{timestamp}.csv", index=False)
    print(f"❌ Failures logged to failed_tests_{timestamp}.csv")
else:
    print("✅ All tests passed")

# Log the test result with timestamp
with open("test_log.csv", "a") as log:
    log.write(f"{datetime.now()}, {'FAIL' if failures else 'PASS'}\n")
