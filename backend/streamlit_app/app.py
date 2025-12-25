
import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path
import os

# Add the project root to the sys.path to import shared modules
# Add the project's main root to sys.path for absolute imports
project_root = Path(__file__).resolve().parents[2] # Go up to fact-check-monitor/
sys.path.insert(0, str(project_root))

from backend.shared.database import Database
from backend.shared.models import FactCheckArticles

# --- Streamlit App --- #
st.set_page_config(layout="wide")
st.title("Fact-Checking Topic Observatory - Data Explorer")

@st.cache_data(ttl=600) # Cache data for 10 minutes
def load_data():
    db = Database()
    with db.get_session() as session:
        articles = session.query(FactCheckArticles).all()
        df = pd.DataFrame([article.__dict__ for article in articles])
        # Drop SQLAlchemy internal state attribute
        if '_s-instance_state' in df.columns:
            df = df.drop(columns=['_s-instance_state'])
        return df

df = load_data()

if df.empty:
    st.warning("No fact-check articles found in the database. Please run the scrapers.")
else:
    st.success(f"Loaded {len(df)} articles from the database.")

    # Convert datetime columns
    df['published_at'] = pd.to_datetime(df['published_at'])

    # Sidebar for filters
    st.sidebar.header("Filters")

    # Medium filter
    all_mediums = ['All'] + sorted(df['medium'].unique().tolist())
    selected_medium = st.sidebar.selectbox("Select Medium", all_mediums)

    # Date range filter
    min_date = df['published_at'].min().date()
    max_date = df['published_at'].max().date()
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = df[(df['published_at'].dt.date >= start_date) & (df['published_at'].dt.date <= end_date)]
    else:
        filtered_df = df.copy()

    if selected_medium != 'All':
        filtered_df = filtered_df[filtered_df['medium'] == selected_medium]

    st.subheader("Filtered Articles Data")
    st.dataframe(filtered_df[['headline', 'medium', 'published_at', 'llm_generated_topic', 'topic', 'url']])

    # --- Visualizations --- #
    st.subheader("Publication Frequency Over Time")
    if not filtered_df.empty:
        freq_df = filtered_df.groupby(pd.Grouper(key='published_at', freq='W')).size().reset_index(name='count')
        fig_freq = px.line(freq_df, x='published_at', y='count', title='Articles Published Per Week')
        st.plotly_chart(fig_freq, use_container_width=True)
    else:
        st.info("No data to display for the selected filters.")

    st.subheader("Topic Distribution")
    if not filtered_df.empty:
        topic_counts = filtered_df['topic'].value_counts().reset_index()
        topic_counts.columns = ['Topic', 'Count']
        fig_topics = px.bar(topic_counts, x='Topic', y='Count', title='Distribution of Consolidated Topics')
        st.plotly_chart(fig_topics, use_container_width=True)

        llm_topic_counts = filtered_df['llm_generated_topic'].value_counts().reset_index()
        llm_topic_counts.columns = ['LLM Generated Topic', 'Count']
        fig_llm_topics = px.bar(llm_topic_counts, x='LLM Generated Topic', y='Count', title='Distribution of LLM Generated Topics')
        st.plotly_chart(fig_llm_topics, use_container_width=True)
    else:
        st.info("No data to display for topic distribution.")


