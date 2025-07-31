import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv("energy_data_india.csv")
st.title("Indian Resedential Energy Dashboard")

region=st.sidebar.selectbox("Select Region",["All"]+ sorted(df["Region"].unique().tolist()) )

if region!="All":
    df=df[df["Region"]==region]

st.subheader("Household energy consumption overview")
st.write(df.head())

avg_energy=df["Monthly_Energy_Consumption_kWh"].mean()
total_energy=df["Monthly_Energy_Consumption_kWh"].sum()
st.metric("Average Monthly Consumption(kWh)",f"{avg_energy:.2f}")
st.metric("Total energy consumption(kWh)",f"{total_energy:.0f}")

st.subheader("Income vs Energy Consumption")
fig1,ax1=plt.subplots()
sns.scatterplot(data=df,x="Monthly_Income_INR",y="Monthly_Energy_Consumption_kWh",hue="Region",ax=ax1)
st.pyplot(fig1)

st.subheader("Appliance-wise Count vs Energy Consumption")
appliances=["Appliance_AC","Appliance_Fan","Appliance_Light","Fridge","Washing_Machine","EV_Charging"]
selected_appliance=st.selectbox("Select Appliance",appliances)
fig2,ax2=plt.subplots()
sns.barplot(x=df[selected_appliance],y=df["Monthly_Energy_Consumption_kWh"],ax=ax2)
ax2.set_xlabel(f"No. of {selected_appliance.replace('_',' ')}")
ax2.set_ylabel("Energy Consumption (kWh)")
st.pyplot(fig2)

st.subheader("Smart Recommendations")
for _, row in df.iterrows():
    if row["Monthly_Energy_Consumption_kWh"]>250:
        st.warning(f"Household ID {row['Household_ID']} - High usage! Recommend switching to solar and LED bulbs.")
    elif row["EV_Charging"]==1:
        st.info(f"Household ID {row['Household_ID']} - installing a separate EV meter for optimal billing.")