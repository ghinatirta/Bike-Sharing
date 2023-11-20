import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

day_df = pd.read_csv('day.csv')

day_df.rename(columns={"instant":"rec_id",
                        "dteday":"datetime",
                        "yr":"year",
                        "mnth":"month",
                        "weathersit":"weather_condition",
                        "casual":"unregistered",
                        "cnt":"total_user"},
              inplace=True)

day_df["datetime"] = pd.to_datetime(day_df.datetime)

day_df["year"] = day_df["month"].map({
    0: "2011", 1:"2012"
})

day_df["season"] = day_df["season"].map({
    1: "Spring", 2:"Summer", 3: "Fall", 4: "Winter"
})
day_df["weather_condition"] = day_df["weather_condition"].map({
    1: "Clear", 2:"Misty/Cloudy", 3: "Light Rain/Snow", 4: "Heavy Rain/Snow"
})

def create_daily_user_df(df):
  daily_user_df = df.groupby(by="datetime").agg({
      "datetime": "nunique",
      "total_user": "sum",
      "unregistered":"sum",
      "registered":"sum"
  })
  daily_user_df = daily_user_df.reset_index(drop=True)
  return daily_user_df

def create_sum_user_df(df):
  sum_user_df = df.groupby("year").total_user.sum().reset_index()
  return sum_user_df

def create_byseason_df(df):
  byseason_df = df.groupby("season").total_user.sum().sort_values(ascending=False).reset_index()
  return byseason_df

def create_byweathercondition_df(df):
  byweathercondition_df = df.groupby("weather_condition").total_user.sum().sort_values(ascending=False).reset_index()
  return byweathercondition_df

def create_bydays_df(df):
  bydays_df = df.groupby("weekday").total_user.sum().reset_index()
  return bydays_df

min_date = pd.to_datetime(day_df["datetime"]).dt.date.min()
max_date = pd.to_datetime(day_df["datetime"]).dt.date.max()

with st.sidebar:
  st.image("https://img.freepik.com/free-vector/couple-bicycle-concept-illustration_114360-4629.jpg?w=740&t=st=1700269258~exp=1700269858~hmac=e4d8bef24f1b2969c57753d123fa10b1ea813c46b1c4c0cac76a934c4b206b90")

  start_date, end_date = st.date_input(
      label="Time Span",
      min_value=min_date,
      max_value=max_date,
      value=[min_date, max_date]
  )

main_df = day_df[(day_df["datetime"] >= str(start_date)) &
                (day_df["datetime"] <= str(end_date))]

daily_user_df = create_daily_user_df(main_df)
sum_user_df = create_daily_user_df(main_df)
byseason_df = create_byseason_df(main_df)
byweathercondition_df = create_byweathercondition_df(main_df)
bydays_df = create_bydays_df(main_df)

st.header('Bike Sharing Dashboard :cloud:')

st.subheader('Bike Sharing User')

col1, col2, col3 = st.columns(3)

with col1:
  total_user = daily_user_df["total_user"].sum()
  st.metric("Total User", value=total_user)

with col2:
  registered_user = daily_user_df["registered"].sum()
  st.metric("Total Registered User", value=registered_user)

with col3:
  unregistered_user = daily_user_df["unregistered"].sum()
  st.metric('Total Unregistered User', value=unregistered_user)


st.subheader("Bike Sharing User in Years")
fig, ax = plt.subplots(figsize=(24, 5))
monthly_user = day_df["total_user"].groupby(day_df["datetime"]).max()
plt.plot(monthly_user.index, monthly_user.values, c="#FF7F50")
plt.xlabel("month")
plt.ylabel("Total")
plt.title("Trend User Bike Sharing")
plt.show()

st.pyplot(fig)

st.subheader("Bike Sharing")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))


sns.barplot(x="total_user", y="season", data=byseason_df, palette="Spectral", ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Season", fontsize=30)
ax[0].set_title("Season Wise", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="total_user", y="weather_condition", data=byweathercondition_df, palette="Spectral", ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Weather Condition", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Weather Wise", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

st.subheader("Bike Sharing for a Week")

fig, ax = plt.subplots(figsize=(20, 10))

sns.barplot(
    y="total_user",
    x="weekday",
    data=bydays_df.sort_values(by="total_user", ascending=False),
    palette="Spectral",
    ax=ax
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.caption('Copyright © Ghina  2023')
