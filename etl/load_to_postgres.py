from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Load the cleaned CSV
df = pd.read_csv("clients_clean.csv")

# Establish connection using env variables
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cur = conn.cursor()

for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO clients_clean (
            client_id,
            first_name,
            last_name,
            email,
            phone,
            join_date,
            risk_level,
            assets_under_management
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (client_id) DO NOTHING;
    """, tuple(row))

conn.commit()
cur.close()
conn.close()

print("Data loaded successfully!")
