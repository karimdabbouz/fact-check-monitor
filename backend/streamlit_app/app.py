import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path
import os

# Add the project root to sys.path for absolute imports
python_project_root = Path(__file__).resolve().parent.parent
if str(python_project_root) not in sys.path:
    sys.path.insert(0, str(python_project_root))

# --- Streamlit App --- #
st.set_page_config(layout="wide", page_title="Fact-Checking Topic Observatory")
st.title("Fact-Checking Topic Observatory")

# Define the path to the CSV file
csv_file = "topic_classification_test.csv"

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_csv_data(csv_path):
    """Load data from the CSV file."""
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df['published_at'] = pd.to_datetime(df['published_at'])
        return df
    else:
        return pd.DataFrame()

# Load data
df = load_csv_data(csv_file)

if df.empty:
    st.warning(f"CSV file '{csv_file}' not found or is empty. Please run `build_topic_classification_csv.py` to generate the data.")
else:
    st.success(f"Loaded {len(df)} articles from {csv_file}")

    # --- Sidebar Filters --- #
    st.sidebar.header("Filters")

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

    # --- Summary Statistics --- #
    total_articles = len(filtered_df)
    st.markdown(f"### 📊 Summary for {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    st.metric("Total Fact-Checks", total_articles)

    # --- Bubble Chart --- #
    if not filtered_df.empty and filtered_df['topic'].notna().sum() > 0:
        # Aggregate by topic
        topic_data = filtered_df[filtered_df['topic'].notna()].groupby('topic').size().reset_index(name='count')
        
        if not topic_data.empty:
            # Calculate percentages
            topic_data['percentage'] = (topic_data['count'] / topic_data['count'].sum() * 100).round(1)
            
            # Create bubble chart using scatter plot
            # Position bubbles in a grid-like pattern for better visualization
            num_topics = len(topic_data)
            
            # Sort by count ascending for horizontal bar chart (bottom to top)
            topic_data = topic_data.sort_values(by='count', ascending=True).reset_index(drop=True)
            
            # Create the bar chart
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                y=topic_data['topic'],
                x=topic_data['count'],
                orientation='h',
                marker=dict(
                    color=topic_data['count'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Article<br>Count")
                ),
                text=topic_data['count'],
                textposition='outside',
                hovertext=[
                    f"<b>{topic}</b><br>Articles: {count}<br>Percentage: {pct}%"
                    for topic, count, pct in zip(topic_data['topic'], topic_data['count'], topic_data['percentage'])
                ],
                hoverinfo='text'
            ))
            
            # Update layout for a cleaner bar chart appearance
            fig.update_layout(
                title="Topic Distribution - Article Count by Domain",
                xaxis_title="Number of Articles",
                yaxis_title="Topic Domain",
                plot_bgcolor='rgba(240, 240, 240, 0.5)',
                hovermode='closest',
                height=600,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # --- Topic Breakdown Table --- #
            st.subheader("Topic Breakdown")
            topic_display = topic_data[['topic', 'count', 'percentage']].copy()
            topic_display.columns = ['Topic', 'Count', 'Percentage (%)']
            topic_display = topic_display.sort_values('Count', ascending=False).reset_index(drop=True)
            st.dataframe(topic_display, use_container_width=True)
        else:
            st.info("No topics available for the selected date range.")
    else:
        st.info("No classified articles found for the selected date range. Please ensure topics are assigned in your data.")
