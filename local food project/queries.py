import sqlite3
import pandas as pd

def run_queries():
    conn = sqlite3.connect("food_waste.db")

    queries = {
        "1. Providers and Receivers count per city":
            """SELECT City, 
                      COUNT(DISTINCT Provider_ID) AS Providers, 
                      COUNT(DISTINCT Receiver_ID) AS Receivers
               FROM Providers 
               LEFT JOIN Receivers USING(City)
               GROUP BY City""",

        "2. Provider type contributing most food":
            """SELECT 
                 CASE 
                     WHEN Provider_Type IS NULL THEN 'Unknown' 
                     ELSE Provider_Type 
                 END AS Provider_Type, 
                 SUM(Quantity) AS Total_Quantity 
             FROM Food_Listings 
             GROUP BY Provider_Type 
             HAVING Total_Quantity IS NOT NULL 
             ORDER BY Total_Quantity DESC""",

        "3. Contact info of Providers in each City":
            """SELECT Name, City, Contact 
               FROM Providers 
               ORDER BY City""",

        "4. Top Receivers by Claims":
            """SELECT Receivers.Name, COUNT(*) AS Total_Claims 
               FROM Claims 
               JOIN Receivers ON Claims.Receiver_ID = Receivers.Receiver_ID 
               GROUP BY Claims.Receiver_ID 
               ORDER BY Total_Claims DESC""",

        "5. Total Quantity Available":
            """SELECT SUM(Quantity) AS Total_Available_Food 
               FROM Food_Listings""",

        "6. City with Most Food Listings":
            """SELECT Location, COUNT(*) AS Listings 
               FROM Food_Listings 
               GROUP BY Location 
               ORDER BY Listings DESC""",

        "7. Most Common Food Types":
            """SELECT Food_Type, COUNT(*) AS Count 
               FROM Food_Listings 
               GROUP BY Food_Type 
               ORDER BY Count DESC""",

        "8. Claims per Food Item":
            """SELECT Food_ID, COUNT(*) AS Claim_Count 
               FROM Claims 
               GROUP BY Food_ID""",

        "9. Provider with Most Successful Claims":
            """SELECT Providers.Name, COUNT(*) AS Success_Count 
               FROM Claims 
               JOIN Food_Listings USING(Food_ID) 
               JOIN Providers ON Food_Listings.Provider_ID = Providers.Provider_ID 
               WHERE Status='Completed' 
               GROUP BY Providers.Provider_ID 
               ORDER BY Success_Count DESC""",

        "10. Claim Status Distribution":
            """SELECT Status, COUNT(*) AS Count 
               FROM Claims 
               GROUP BY Status""",

        "11. Average Quantity Claimed per Receiver":
            """SELECT Receivers.Name, AVG(Food_Listings.Quantity) AS Avg_Claimed 
               FROM Claims 
               JOIN Food_Listings USING(Food_ID) 
               JOIN Receivers ON Claims.Receiver_ID = Receivers.Receiver_ID 
               GROUP BY Claims.Receiver_ID""",

        "12. Most Claimed Meal Type":
            """SELECT Meal_Type, COUNT(*) AS Count 
               FROM Food_Listings 
               JOIN Claims USING(Food_ID) 
               GROUP BY Meal_Type 
               ORDER BY Count DESC""",

        "13. Total Food Donated by Provider":
            """SELECT Providers.Name, SUM(Quantity) AS Total_Donated 
               FROM Food_Listings 
               JOIN Providers USING(Provider_ID) 
               GROUP BY Provider_ID""",

        "14. Expiring Food Items (Near expiry)":
            """SELECT Food_Name, Expiry_Date 
               FROM Food_Listings 
               WHERE DATE(Expiry_Date) < DATE('now', '+3 days')""",

        "15. Receivers in each City needing food":
            """SELECT City, COUNT(*) AS Total_Receivers 
               FROM Receivers 
               GROUP BY City"""
    }

    result = {}
    for title, q in queries.items():
        result[title] = pd.read_sql_query(q, conn)

    conn.close()
    return result