import streamlit as st
import pandas as pd
from pymongo import MongoClient
import datetime as dt

# Function to connect to MongoDB
def connect_to_mongodb(collection_name):

    username = st.secrets["MongoDB"]["mongo_username"]
    password = st.secrets["MongoDB"]["mongo_password"]
    cluster_url = st.secrets["MongoDB"]["mongo_cluster_url"]
    client = MongoClient(f"mongodb+srv://{username}:{password}@{cluster_url}/")
    db = client[st.secrets["MongoDB"]["DATABASE_NAME"]]
    collection = db[collection_name]
    return collection

# Function to get the player ids
def get_player_ids():
    collection = connect_to_mongodb("roster")
    df = pd.DataFrame(list(collection.find()))
    return df["player_id"]

# Function to write the RPE data to the database collection
def write_rpe_data():
    collection = connect_to_mongodb()

# ------------------------------------------------------------
# Main Streamlit app
# ------------------------------------------------------------

# Basic page setup
st.set_page_config(page_title="RPE data collector", page_icon=":lightbulb:", layout="centered")

st.title("RPE data collector")

tab1, tab2 = st.tabs(["Enter RPE scores", "Borg scale info"])

# Function to format the player_ids as integers
def format_as_integer(number):
    return int(number)

# RPE data entry form
with tab1:
    # Data input fields
    player_id = st.selectbox("Player ID", options=get_player_ids(),format_func=format_as_integer)
    session_date = st.date_input("Session date", format="DD/MM/YYYY")
    before = st.radio("How did you feel before the session?", options=["0","1","2","3","4","5","6","7","8","9","10"], horizontal=True)
    after = st.radio("How did you feel after the session?", options=["0","1","2","3","4","5","6","7","8","9","10"], horizontal=True)
    intensity = st.radio("How do you rate the intensity of the session?", options=["0","1","2","3","4","5","6","7","8","9","10"], horizontal=True)
    partial_session = st.toggle("Partial/Individual session", value=False)
    if partial_session:
        individual_session = st.checkbox("Individual session", value=False)
        session_duration = st.number_input("Minutes", min_value=1, value=1, step=1)
    else:
        individual_session = False
        session_duration = 0
    comments = st.text_input("Comments")

    # Submitting the form
    submitted = st.button("Save data")

    if submitted:
        # Update the MongoDB collection with the new RPE record
        try:
            # Create the new record dictionary with user input
            new_rpe_entry = {   "player_id": player_id,
                                "session_id": int(session_date.strftime("%Y%m%d")),
                                "before": before,
                                "after": after,
                                "intensity": intensity,
                                "part_ind_session": partial_session,
                                "individual_session": individual_session,
                                "session_duration": session_duration,
                                "comments": comments }
        
            # Connect to the database
            collection = connect_to_mongodb("rpe_form_data")
            collection.insert_one(new_rpe_entry)  # Insert the RPE record
            st.success("Your RPE data was succsfully saved.")
            st.balloons()

        except:
            st.error("Connection error. Could not save your RPE data.")

# RPE Borg scale explanation
with tab2:
    st.subheader("Borg scale of perceived excertion")
    st.write("Use the 10 point Borg scale of Percieved Excertion below to rate your training session.")
    st.image("borg_scale_image.jpg")
