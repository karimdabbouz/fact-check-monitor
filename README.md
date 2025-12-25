# Fact-Checking Topic Observatory

## Project Overview

This project aims to analyze fact-checking journalism as a corpus, making visible the narratives and claims being fought over in public discourse. Instead of building another fact-check site, this platform provides a meta-layer over fact checks, allowing users to observe agenda-setting, framing, and potential imbalances in fact-checking focus.

## Core Question

"What is being fact-checked — and what does that say about public discourse?"

## Multi-Axis Classification Model

To provide a nuanced understanding of fact-checked claims, the project employs a multi-axis classification model:

- **Axis 1: Supervised Topic Label (Domain)**
    - This represents the overall societal domain a fact-check belongs to. These labels are stable, small in number, and used for statistics, trends, and visualizations.
    - **Current Axis 1 Topics:**
        - Migration
        - Demokratie & Wahlen
        - Politik & Regierung
        - Medien & Öffentlichkeit
        - Umwelt & Klima
        - Gesundheit
        - Krieg & Konflikte
        - Kriminalität & Sicherheit
        - Technologie
        - Wirtschaft & Soziales
        - Verbraucherthemen

- **Axis 2: The Claim Being Fact-Checked**
    - This is a one-sentence summary of the false or misleading claim that was fact-checked. It captures nuance without fragmenting statistics.

- **Axis 3: Instrumentalizer**
    - This identifies the person, party, organization, media ecosystem, or state actor who used, spread, or benefited from the claim.

- **Axis 4: Entities Involved**
    - These are broad entity extractions (persons, organizations, countries, institutions) that are part of the false claim.

## Technical Stack

- **Backend:** Python + FastAPI
- **Database:** PostgreSQL
- **Frontend (Planned):** SvelteKit
- **Scrapers:** Custom Python scrapers for fact-checking outlets.
- **Topic Generation:** LLMs are used for initial unsupervised semantic categorization, followed by human-in-the-loop consolidation for stable topic labels.

## Current Status

- Approximately 500 fact-check articles in the database.
- Unsupervised LLM topic labeling has been run.
- Topic list consolidated manually into domains.
- Multi-axis framework conceptualized and partly implemented (Axis 1).
- MVP scope is clear.
- Frontend design is ready to start.

## Development Environment

### Streamlit Data Explorer

A Streamlit application is available in `backend/streamlit_app/app.py` for local development. This app allows for visual exploration of the fact-check data, including publication frequency and topic distributions, and can be used to sketch out frontend features.

**To run the Streamlit app:**

1.  Navigate to the `backend/streamlit_app` directory:
    ```bash
    cd backend/streamlit_app
    ```
2.  Install dependencies (if not already installed):
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the app:
    ```bash
    streamlit run app.py
    ```


