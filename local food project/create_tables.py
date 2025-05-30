import sqlite3
import pandas as pd

# Database connect karo (ya create hoga agar nahi hai to)
conn = sqlite3.connect("food_waste.db")
cursor = conn.cursor()

# 1️⃣ Drop if already exist & Create Providers Table
cursor.execute("DROP TABLE IF EXISTS Providers")
cursor.execute("""
    CREATE TABLE Providers (
        Provider_ID INTEGER PRIMARY KEY,
        Name TEXT,
        Type TEXT,
        Address TEXT,
        City TEXT,
        Contact TEXT
    )
""")

# 2️⃣ Create Receivers Table
cursor.execute("DROP TABLE IF EXISTS Receivers")
cursor.execute("""
    CREATE TABLE Receivers (
        Receiver_ID INTEGER PRIMARY KEY,
        Name TEXT,
        Type TEXT,
        City TEXT,
        Contact TEXT
    )
""")

# 3️⃣ Create Food_Listings Table
cursor.execute("DROP TABLE IF EXISTS Food_Listings")
cursor.execute("""
    CREATE TABLE Food_Listings (
        Food_ID INTEGER PRIMARY KEY,
        Food_Name TEXT,
        Quantity INTEGER,
        Expiry_Date TEXT,
        Provider_ID INTEGER,
        Provider_Type TEXT,
        Location TEXT,
        Food_Type TEXT,
        Meal_Type TEXT,
        FOREIGN KEY (Provider_ID) REFERENCES Providers(Provider_ID)
    )
""")

# 4️⃣ Create Claims Table
cursor.execute("DROP TABLE IF EXISTS Claims")
cursor.execute("""
    CREATE TABLE Claims (
        Claim_ID INTEGER PRIMARY KEY,
        Food_ID INTEGER,
        Receiver_ID INTEGER,
        Status TEXT,
        Timestamp TEXT,
        FOREIGN KEY (Food_ID) REFERENCES Food_Listings(Food_ID),
        FOREIGN KEY (Receiver_ID) REFERENCES Receivers(Receiver_ID)
    )
""")

# ✅ Load CSV files
providers = pd.read_csv("data/providers_data.csv")
receivers = pd.read_csv("data/receivers_data.csv")
food_listings = pd.read_csv("data/food_listings_data.csv")
claims = pd.read_csv("data/claims_data.csv")

# ✅ Insert into tables
providers.to_sql("Providers", conn, if_exists="append", index=False)
receivers.to_sql("Receivers", conn, if_exists="append", index=False)
food_listings.to_sql("Food_Listings", conn, if_exists="append", index=False)
claims.to_sql("Claims", conn, if_exists="append", index=False)

print("✅ Tables created and data loaded successfully.")

# 🔚 Close connection
conn.commit()
conn.close()
