# 🍛 Local Food Wastage Management System

A socially impactful data-driven web application built using **Python**, **SQL**, and **Streamlit** that helps connect food providers (like restaurants) with food receivers (like NGOs and individuals), aiming to reduce local food wastage.

---

## 🚀 Live Demo
👉 [Click here to view the deployed app](https://your-deployment-link.streamlit.app)  
*(Replace with your actual link after deployment)*

---

## 🧰 Tech Stack

- 🐍 Python
- 🗃️ SQLite (SQL Database)
- 📊 Streamlit (Web Interface)
- 📈 Pandas + Matplotlib (Data Analysis & Visualization)

---

## 📂 Datasets Used

| Dataset              | Description                        |
|----------------------|------------------------------------|
| `providers_data.csv` | Restaurants & food providers info  |
| `receivers_data.csv` | NGOs & people who receive food     |
| `food_listings_data.csv` | Surplus food listings             |
| `claims_data.csv`    | Track of food claimed by receivers |

---

## 🎯 Features

- ✅ **SQL Query Panel**: 15+ SQL insights (e.g. top cities, food types)
- 🔍 **Filter View**: Filter by city, meal type, food type
- 📝 **CRUD Panel**: Add/Delete new food listings
- 📞 **Contact Panel**: Find provider contact by city
- 🛒 **Claim Panel**: Food can be claimed by verified receivers
- 📈 **Charts**: Visualize food trends via pie & bar charts
- ☁️ **Live Deployment**: Hosted on Streamlit Cloud

---

## 📊 Sample SQL Questions Answered

- How many providers & receivers in each city?
- Which food types are donated most?
- Which provider has maximum successful food claims?
- What % of claims are pending/completed/canceled?
- Which meal type is most demanded?

---

## 🛠️ How to Run Locally

```bash
git clone https://github.com/yourusername/local-food-wastage-app
cd local-food-wastage-app

# Install dependencies
pip install -r requirements.txt

# Load data
python create_tables.py

# Run the app
streamlit run app.py
