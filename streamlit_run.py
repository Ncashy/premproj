import os
import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client, Client
from dotenv import load_dotenv
import seaborn as sns
import matplotlib.pyplot as plt

# Load .env credentials
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Streamlit Title
st.title("Premier League Players Dashboard")
st.header("About the Dataset")

# Load data from Supabase (cached)
@st.cache_data
def load_data(limit=1000):
    response = supabase.table("plp").select("*").limit(limit).execute()
    return pd.DataFrame(response.data)

# Show loading text
st.text("Loading data from Supabase...")
data = load_data()
st.success(f"Loaded {len(data)} rows!")

# Checkbox to show raw data (with unique key to avoid Streamlit ID conflict)
if st.checkbox("Show raw data", key="raw_data_pl"):
    st.subheader("Raw Premier League Players Data")
    st.write(data)

# Filter by Club
clubs = sorted(data['club'].dropna().unique())
selected_club = st.selectbox("Filter by Club", options=["All"] + clubs)

if selected_club != "All":
    filtered_data = data[data['club'] == selected_club]
else:
    filtered_data = data

st.write(f"Showing {len(filtered_data)} players")

# --- CHART 1: Goals per Match Distribution ---
if 'goals_per_match' in filtered_data.columns:
    st.subheader("Goals per Match Distribution")
    st.bar_chart(filtered_data['goals_per_match'].dropna())



# --- CHART 3: Position Count ---
if 'position' in filtered_data.columns:
    st.subheader("Player Position Breakdown")
    
    position_counts = filtered_data['position'].value_counts().reset_index()
    position_counts.columns = ['Position', 'Count']
    
    fig2 = px.bar(
        position_counts,
        x='Position',
        y='Count',
        title="Distribution by Position",
        text='Count',
        color='Position'  # Optional: adds color per bar
    )
    
    st.plotly_chart(fig2)


#"Shooting Accuracy vs Goals") # change graph type 
if all(col in filtered_data.columns for col in ['shooting_accuracy_percent', 'goals', 'shots_on_target']):
    st.subheader("Shooting Accuracy vs Goals")

    # Drop rows with NaNs in any required columns
    valid_data = filtered_data.dropna(subset=['shooting_accuracy_percent', 'goals', 'shots_on_target'])

    if not valid_data.empty:
        fig = px.scatter(
            valid_data,
            x='shooting_accuracy_percent',
            y='goals',
            color='club',
            hover_name='name',
            size='shots_on_target',
            title="Shooting Accuracy vs Goals"
        )
        st.plotly_chart(fig)
    else:
        st.warning("No valid data available for shooting accuracy, goals, and shots on target.")

# --- CHART 5: Tackles vs Interceptions --- chaneg graph type 
if all(col in filtered_data.columns for col in ['tackles', 'interceptions', 'tackle_success_%']):
    st.subheader("Tackles vs Interceptions")
    fig = px.scatter(
        filtered_data.dropna(subset=['tackles', 'interceptions', 'tackle_success_%']),
        x='tackles',
        y='interceptions',
        color='position',
        hover_name='name',
        size='tackle_success_%',
        title="Tackles vs Interceptions"
    )
    st.plotly_chart(fig)

# --- CHART 6: Goalkeeper Performance ---
if all(col in filtered_data.columns for col in ['saves', 'goals_conceded']):
    st.subheader("Goalkeeper Performance: Saves vs Goals Conceded")
    
    # Filter likely goalkeepers (where saves is not null or > 0)
    gk_data = filtered_data[(filtered_data['saves'] > 0) | (filtered_data['goals_conceded'] > 0)]
    
    if not gk_data.empty:
        fig = px.scatter(
            gk_data,
            x='saves',
            y='goals_conceded',
            color='club',
            hover_name='name',
            title="Saves vs Goals Conceded (Goalkeepers)"
        )
        st.plotly_chart(fig)
    else:
        st.info("No goalkeeper data available for selected filter.")
# countreies most repsesentated
if 'nationality' in filtered_data.columns:
    st.subheader("Top Nationalities in the Premier League")

    nationality_counts = (
        filtered_data['nationality']
        .dropna()
        .value_counts()
        .nlargest(10)
        .reset_index()
    )
    nationality_counts.columns = ['nationality', 'player_count']

    fig = px.bar(
        nationality_counts,
        x='player_count',
        y='nationality',
        orientation='h',
        title="Top 10 Most Represented Countries in the EPL",
        text='player_count',
        color='nationality'
    )

    fig.update_layout(yaxis=dict(categoryorder='total ascending'))
    st.plotly_chart(fig)
else:
    st.warning("The 'nationality' column is not present in the dataset.")

#player stat by player
if all(col in filtered_data.columns for col in ['position', 'goals', 'assists']):
    st.subheader("Player Stats by Position")

    stats_by_position = (
        filtered_data
        .groupby('position')[['goals', 'assists']]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        stats_by_position.melt(id_vars='position', value_vars=['goals', 'assists']),
        x='position',
        y='value',
        color='variable',
        barmode='group',
        title="Average Goals and Assists by Position"
    )
    st.plotly_chart(fig)

#3️ Top Players by Position Factors
st.subheader("Top Players by Position")

# For example, top midfielders by assists
top_mids = filtered_data[filtered_data['position'] == 'Midfielder']
top_mids = top_mids.sort_values(by='assists', ascending=False).head(10)

fig = px.bar(
    top_mids,
    x='assists',
    y='name',
    orientation='h',
    title='Top 10 Midfielders by Assists',
    color='club',
    text='assists'
)
st.plotly_chart(fig)
#players at risk 
risk_columns = ['red_cards', 'big_chances_missed', 'errors_leading_to_goal', 'own_goals']

for col in risk_columns:
    if col in filtered_data.columns:
        st.subheader(f"Top 10 Players by {col.replace('_', ' ').title()}")
        top_risk = filtered_data[['name', 'club', col]].sort_values(by=col, ascending=False).head(10)
        
        fig = px.bar(
            top_risk,
            x=col,
            y='name',
            orientation='h',
            color='club',
            text=col,
            title=f"Top 10 Players by {col.replace('_', ' ').title()}"
        )
        st.plotly_chart(fig)
#top contributions 


st.subheader("Top 10 Players by Total Contributions")

if all(col in filtered_data.columns for col in ['goals', 'assists']):
    filtered_data['Total Contributions'] = filtered_data['goals'] + filtered_data['assists']
    total_contributions = filtered_data.sort_values(by='Total Contributions', ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    palette = sns.color_palette("crest", 10)[::-1]
    sns.barplot(
        x='Total Contributions',
        y='name',
        data=total_contributions,
        palette=palette
    )
    plt.title("Top 10 Contribution Players")
    
    for index, value in enumerate(total_contributions['Total Contributions']):
        plt.text(value, index, str(value), va='center')

    st.pyplot(plt.gcf())
#image 
st.image("https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.independent.co.uk%2Fsport%2Ffootball%2Fpremier-league%2Fpremier-league-logo-blimey-the-new-design-is-sleek-clean-and-clever-a6863591.html&psig=AOvVaw3JCUP3JXebMe9RxBL5atk_&ust=1758594831410000&source=images&cd=vfe&opi=89978449&ved=0CBYQjRxqFwoTCIj6gbuq648DFQAAAAAdAAAAABAE", width=150)

# Final data table
st.subheader("Filtered Player Data")
st.dataframe(filtered_data)
