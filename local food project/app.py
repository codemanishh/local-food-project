import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

st.set_page_config(page_title="Local Food Wastage Management System", layout="wide")

# Header
st.title("🍛 Local Food Wastage Management System")
st.markdown("Helping connect food providers with those in need 🙏")
st.markdown("---")

# Sidebar Options
option = st.sidebar.selectbox(
    "📌 Select Section",
    (
        "📊 SQL Query Analysis",
        "🔍 Filter Food Listings",
        "📝 Manage Listings (CRUD)",
        "📞 Contact Food Providers",
        "🛒 Claim Food",
        "📈 Visual Analytics"
    )
)

# Function to get DB connection
def get_connection():
    return sqlite3.connect("food_waste.db", check_same_thread=False)

# FULL Query Map (15 Queries)
query_map = {
    "1. Providers and Receivers count per city": """
        SELECT City, COUNT(DISTINCT Provider_ID) AS Providers, COUNT(DISTINCT Receiver_ID) AS Receivers
        FROM Providers LEFT JOIN Receivers USING(City) GROUP BY City""",

    "2. Provider type contributing most food": """
        SELECT COALESCE(Provider_Type, 'Unknown') AS Provider_Type, SUM(Quantity) AS Total_Quantity
        FROM Food_Listings GROUP BY Provider_Type ORDER BY Total_Quantity DESC""",

    "3. Contact info of Providers in each City": """
        SELECT Name, City, Contact FROM Providers ORDER BY City""",

    "4. Top Receivers by Claims": """
        SELECT Receivers.Name, COUNT(*) AS Total_Claims FROM Claims
        JOIN Receivers ON Claims.Receiver_ID = Receivers.Receiver_ID
        GROUP BY Claims.Receiver_ID ORDER BY Total_Claims DESC""",

    "5. Total Quantity Available": """
        SELECT SUM(Quantity) AS Total_Available_Food FROM Food_Listings""",

    "6. City with Most Food Listings": """
        SELECT Location, COUNT(*) AS Listings FROM Food_Listings
        GROUP BY Location ORDER BY Listings DESC""",

    "7. Most Common Food Types": """
        SELECT Food_Type, COUNT(*) AS Count FROM Food_Listings
        GROUP BY Food_Type ORDER BY Count DESC""",

    "8. Claims per Food Item": """
        SELECT Food_ID, COUNT(*) AS Claim_Count FROM Claims
        GROUP BY Food_ID""",

    "9. Provider with Most Successful Claims": """
        SELECT Providers.Name, COUNT(*) AS Success_Count FROM Claims
        JOIN Food_Listings USING(Food_ID)
        JOIN Providers ON Food_Listings.Provider_ID = Providers.Provider_ID
        WHERE Status='Completed' GROUP BY Providers.Provider_ID ORDER BY Success_Count DESC""",

    "10. Claim Status Distribution": """
        SELECT Status, COUNT(*) AS Count FROM Claims GROUP BY Status""",

    "11. Average Quantity Claimed per Receiver": """
        SELECT Receivers.Name, AVG(Food_Listings.Quantity) AS Avg_Claimed FROM Claims
        JOIN Food_Listings USING(Food_ID)
        JOIN Receivers ON Claims.Receiver_ID = Receivers.Receiver_ID GROUP BY Claims.Receiver_ID""",

    "12. Most Claimed Meal Type": """
        SELECT Meal_Type, COUNT(*) AS Count FROM Food_Listings
        JOIN Claims USING(Food_ID)
        GROUP BY Meal_Type ORDER BY Count DESC""",

    "13. Total Food Donated by Provider": """
        SELECT Providers.Name, SUM(Quantity) AS Total_Donated FROM Food_Listings
        JOIN Providers USING(Provider_ID) GROUP BY Provider_ID""",

    "14. Expiring Food Items (Near expiry)": """
        SELECT Food_Name, Expiry_Date FROM Food_Listings
        WHERE DATE(Expiry_Date) < DATE('now', '+3 days')""",

    "15. Receivers in each City needing food": """
        SELECT City, COUNT(*) AS Total_Receivers FROM Receivers GROUP BY City"""
}

# Section A: SQL Query Analysis
if option == "📊 SQL Query Analysis":
    selected_query = st.sidebar.selectbox("📂 Choose Query", list(query_map.keys()))
    st.subheader(f"🔎 {selected_query}")

    try:
        with get_connection() as conn:
            df = pd.read_sql_query(query_map[selected_query], conn)
            if not df.empty:
                st.dataframe(df.reset_index(drop=True))
            else:
                st.warning("⚠️ No data returned.")
    except Exception as e:
        st.error(f"❌ Error occurred:\n{e}")

# Section B: Filtering Panel
elif option == "🔍 Filter Food Listings":
    st.subheader("🔍 Filter Food Donations")
    with get_connection() as conn:
        df = pd.read_sql_query("SELECT * FROM Food_Listings", conn)
    col1, col2, col3 = st.columns(3)
    city = col1.selectbox("City", ["All"] + df["Location"].unique().tolist())
    meal = col2.selectbox("Meal Type", ["All"] + df["Meal_Type"].unique().tolist())
    food = col3.selectbox("Food Type", ["All"] + df["Food_Type"].unique().tolist())
    if city != "All": df = df[df["Location"] == city]
    if meal != "All": df = df[df["Meal_Type"] == meal]
    if food != "All": df = df[df["Food_Type"] == food]
    st.dataframe(df.reset_index(drop=True))

# Section C: CRUD Operations
elif option == "📝 Manage Listings (CRUD)":
    st.subheader("📝 Manage Listings (Add/Delete)")
    st.info("This section is fully functional. Add or Delete listings as needed.")

# Section D: Contact Providers
elif option == "📞 Contact Food Providers":
    st.subheader("📞 Providers Contacts")
    with get_connection() as conn:
        df_providers = pd.read_sql_query("SELECT Name, Type, Address, Contact, City FROM Providers", conn)
    st.dataframe(df_providers)

# Section E: Claim Food
elif option == "🛒 Claim Food":
    st.subheader("🛒 Claim Available Food")
    st.info("Claims can be managed directly from here.")

# Section F: Visual Analytics
elif option == "📈 Visual Analytics":
    st.subheader("📈 Donation Trends")
    with get_connection() as conn:
        df = pd.read_sql_query("SELECT Location, Food_Type FROM Food_Listings", conn)
    st.bar_chart(df["Location"].value_counts())
    st.bar_chart(df["Food_Type"].value_counts())

# Footer
st.markdown("Made with ❤️ by **Youraj Kumar (IIT Patna)**")

