from sqlalchemy import create_engine

# Your connection string
DATABASE_URL = "postgresql://postgres:root@localhost/bankdb"

try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("✅ Connected to PostgreSQL successfully!")
    connection.close()
except Exception as e:
    print("❌ Failed to connect:", e)
