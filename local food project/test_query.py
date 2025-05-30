import sqlite3
import pandas as pd

# Connect to your database
conn = sqlite3.connect("food_waste.db")

# Query you want to test
query = """
SELECT 
   COALESCE(Provider_Type, 'Unknown') AS Provider_Type, 
   SUM(Quantity) AS Total_Quantity 
FROM Food_Listings 
GROUP BY Provider_Type 
HAVING Total_Quantity IS NOT NULL 
ORDER BY Total_Quantity DESC
"""

# Run the query and show output
df = pd.read_sql_query(query, conn)
print(df)