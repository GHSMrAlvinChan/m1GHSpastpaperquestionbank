import streamlit as st

# --- Simulated Data (Replace with actual file loading if needed for deployment) ---
# In a real scenario, you might load these from a database, a structured file (CSV/JSON),
# or dynamically read from specific .txt files based on a naming convention.
# For this example, we'll use an in-memory list of dictionaries.

# Each dictionary represents a 'document' or 'text file' with its associated metadata
simulated_documents = [
    {"topic": "A", "level": 1, "year": 2020, "content": "Document 1: Introduction to Topic A, focusing on fundamental concepts for Level 1, as taught in the year 2020."},
    {"topic": "A", "level": 2, "year": 2021, "content": "Document 2: Advanced theories in Topic A. This content covers more complex ideas suitable for Level 2, updated in 2021."},
    {"topic": "A", "level": 3, "year": 2022, "content": "Document 3: Cutting-edge research in Topic A. Designed for Level 3 experts, reflecting 2022's latest findings."},
    {"topic": "B", "level": 1, "year": 2019, "content": "Document 4: Basics of Topic B. Practical skills for beginners at Level 1, from 2019."},
    {"topic": "B", "level": 2, "year": 2020, "content": "Document 5: Applied methodologies in Topic B. Intermediate concepts for Level 2, developed in 2020."},
    {"topic": "B", "level": 3, "year": 2023, "content": "Document 6: Strategic implementations in Topic B. High-level analysis for Level 3, released in 2023."},
    {"topic": "C", "level": 1, "year": 2021, "content": "Document 7: Core principles of Topic C. Foundational knowledge for Level 1, from 2021."},
    {"topic": "C", "level": 2, "year": 2022, "content": "Document 8: Analytical techniques in Topic C. Suitable for Level 2, published in 2022."},
    {"topic": "C", "level": 3, "year": 2024, "content": "Document 9: Future directions in Topic C. Very advanced material for Level 3, hot off the press from 2024."},
    {"topic": "A", "level": 1, "year": 2021, "content": "Document 10: Supplemental material for Topic A, Level 1. This covers additional examples from 2021."},
    {"topic": "B", "level": 1, "year": 2021, "content": "Document 11: Another introductory text for Topic B, Level 1, published in 2021."},
    {"topic": "C", "level": 2, "year": 2023, "content": "Document 12: Case studies for Topic C, Level 2, from 2023."},
]

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="M1 Past Paper Questions Generator",
    layout="wide",
    initial_sidebar_state="expanded" # Keep sidebar expanded by default
)

# --- Sidebar for Filters ---
st.sidebar.header("Filter Content")

st.sidebar.subheader("Select Topics")
selected_topics = []
if st.sidebar.checkbox("Topic A", value=True): # Default selected
    selected_topics.append("A")
if st.sidebar.checkbox("Topic B"):
    selected_topics.append("B")
if st.sidebar.checkbox("Topic C"):
    selected_topics.append("C")

st.sidebar.subheader("Select Levels")
selected_levels = []
if st.sidebar.checkbox("Level 1", value=True): # Default selected
    selected_levels.append(1)
if st.sidebar.checkbox("Level 2"):
    selected_levels.append(2)
if st.sidebar.checkbox("Level 3"):
    selected_levels.append(3)

st.sidebar.subheader("Select Years")
# Get the range of years from your simulated data for the slider
min_year = min(doc["year"] for doc in simulated_documents)
max_year = max(doc["year"] for doc in simulated_documents)
selected_years = st.sidebar.slider(
    "Number of Years (Range)",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year), # Default to full range
    step=1
)
st.sidebar.info(f"Selected Year Range: {selected_years[0]} - {selected_years[1]}")


# --- Main Content Area ---
st.title("📚 M1 Past Paper Questions Generator")
st.markdown("""
Use the filters in the sidebar to dynamically search and display relevant text content.
This app simulates extracting information from various documents based on your criteria.
""")

# Button to trigger search explicitly (Streamlit also re-runs on widget changes)
if st.button("Apply Filters and Search"):
    st.session_state.search_triggered = True

# Initialize search_triggered state if not present
if 'search_triggered' not in st.session_state:
    st.session_state.search_triggered = False

if st.session_state.search_triggered:
    st.header("Search Results")

    # --- Filtering Logic ---
    filtered_documents = []
    for doc in simulated_documents:
        # Check if topic matches
        topic_match = doc["topic"] in selected_topics

        # Check if level matches
        level_match = doc["level"] in selected_levels

        # Check if year is within the selected range
        year_match = selected_years[0] <= doc["year"] <= selected_years[1]

        if topic_match and level_match and year_match:
            filtered_documents.append(doc)

    # --- Display Results ---
    if filtered_documents:
        st.success(f"Found {len(filtered_documents)} document(s) matching your criteria:")
        for i, doc in enumerate(filtered_documents):
            with st.expander(f"**Topic: {doc['topic']} | Level: {doc['level']} | Year: {doc['year']}**"):
                st.write(doc["content"])
                # You could add a download button for each document here if they were actual files
                # For example:
                # st.download_button(
                #     label=f"Download Doc {i+1}",
                #     data=doc["content"],
                #     file_name=f"document_{doc['topic']}_{doc['level']}_{doc['year']}_{i+1}.txt",
                #     mime="text/plain"
                # )
    else:
        st.warning("No documents found matching your selected criteria. Please adjust your filters.")

st.markdown("---")
st.info("💡 Tip: Changes to the filters in the sidebar will automatically re-run the search (or click 'Apply Filters and Search').")
