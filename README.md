# ETL Data Quality Tests

This project contains automated data quality tests for an ETL (Extract, Transform, Load) pipeline.  
It is designed to ensure accurate, complete, and timely data transformation for reporting or analytics environments.

---

## ✅ Features

- Rank validation (Top 5 transactions per user)
- Null checks (Ensure usernames are not missing)
- Freshness checks (Only recent data is processed)
- Logging of failed test cases to CSV
- Summary logging of test results with timestamps

---

## 🛠️ Tech Stack

- Python
- pandas
- psycopg2
- dotenv
- PostgreSQL 

---

## 🚀 How to Use

1. **Clone this repo**
   ```bash
   git clone https://github.com/BrianBaguma92/etl-sample-test.git
   cd YOUR_REPO
