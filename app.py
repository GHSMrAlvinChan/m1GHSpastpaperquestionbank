import streamlit as st

# --- Simulated Data (Replace with actual file loading if needed for deployment) ---
# In a real scenario, you might load these from a database, a structured file (CSV/JSON),
# or dynamically read from specific .txt files based on a naming convention.
# For this example, we'll use an in-memory list of dictionaries.

# Each dictionary represents a 'document' or 'text file' with its associated metadata
simulated_documents = [
    {"topic": "A", "level": 1, "year": 2020, "content": "Question 1: Derive the equations of motion for a particle under constant acceleration. (Topic A, Level 1, 2020)"},
    {"topic": "A", "level": 2, "year": 2021, "content": "Question 2: A block of mass 'm' is pulled along a rough horizontal surface by a force 'F' at an angle 'theta' to the horizontal. Calculate the acceleration of the block. (Topic A, Level 2, 2021)"},
    {"topic": "A", "level": 3, "year": 2022, "content": "Question 3: A particle moves in a straight line such that its velocity 'v' at time 't' is given by v = 3t^2 - 6t. Find the total distance travelled by the particle in the first 3 seconds. (Topic A, Level 3, 2022)"},
    {"topic": "B", "level": 1, "year": 2019, "content": "Question 4: State Newton's three laws of motion. (Topic B, Level 1, 2019)"},
    {"topic": "B", "level": 2, "year": 2020, "content": "Question 5: A force of (3i + 4j) N acts on a particle. Find the magnitude of this force. (Topic B, Level 2, 2020)"},
    {"topic": "B", "level": 3, "year": 2023, "content": "Question 6: Two particles, P and Q, are moving towards each other along a straight line. Given their initial velocities and the coefficient of restitution, calculate their velocities after impact. (Topic B, Level 3, 2023)"},
    {"topic": "C", "level": 1, "year": 2021, "content": "Question 7: Define momentum and impulse. (Topic C, Level 1, 2021)"},
    {"topic": "C", "level": 2, "year": 2022, "content": "Question 8: A bullet of mass 'm' is fired into a block of mass 'M' which is initially at rest. The bullet becomes embedded in the block. Calculate the common velocity of the bullet and block immediately after impact. (Topic C, Level 2, 2022)"},
    {"topic": "C", "level": 3, "year": 2024, "content": "Question 9: A car of mass 1200 kg is travelling up a hill inclined at an angle 'alpha' to the horizontal. The engine produces a constant power P. Given the resistance to motion, find the maximum speed the car can attain. (Topic C, Level 3, 2024)"},
    {"topic": "A", "level": 1, "year": 2021, "content": "Question 10: Illustrate the difference between speed and velocity with examples. (Topic A, Level 1, 2021)"},
    {"topic": "B", "level": 1, "year": 2021, "content": "Question 11: Explain the concept of weightlessness in orbit. (Topic B, Level 1, 2021)"},
    {"topic": "C", "level": 2, "year": 2023, "content": "Question 12: A ball is thrown vertically upwards from the ground with an initial speed of U m/s. Find the time taken to reach its maximum height. (Topic C, Level 2, 2023)"},
]

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="M1 Past Paper Questions Generator", # NEW: Changed page title
    layout="wide",
    initial_sidebar_state="expanded" # Keep sidebar expanded by default
)

# --- Sidebar for Filters ---
st.sidebar.header("Filter Questions")

st.sidebar.subheader("Select Topics")
selected_topics = []
if st.sidebar.checkbox("Topic A (Kinematics)", value=True): # Default selected
    selected_topics.append("A")
if st.sidebar.checkbox("Topic B (Forces & Newton's Laws)"):
    selected_topics.append("B")
if st.sidebar.checkbox("Topic C (Momentum & Energy)"):
    selected_topics.append("C")

st.sidebar.subheader("Select Difficulty Levels")
selected_levels = []
if st.sidebar.checkbox("Level 1 (Basic)", value=True): # Default selected
    selected_levels.append(1)
if st.sidebar.checkbox("Level 2 (Intermediate)"):
    selected_levels.append(2)
if st.sidebar.checkbox("Level 3 (Advanced)"):
    selected_levels.append(3)

st.sidebar.subheader("Select Years")
# Get the range of years from your simulated data for the slider
min_year = min(doc["year"] for doc in simulated_documents)
max_year = max(doc["year"] for doc in simulated_documents)
selected_years = st.sidebar.slider(
    "Year Range of Questions",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year), # Default to full range
    step=1
)
st.sidebar.info(f"Selected Year Range: {selected_years[0]} - {selected_years[1]}")


# --- Main Content Area ---
st.title("M1 Past Paper Questions Generator") # NEW: Changed main title
st.markdown("""
Welcome to the **M1 Past Paper Questions Generator**! Use the filters in the sidebar to dynamically
select and display relevant past paper questions based on specific topics, difficulty levels, and
years. This helps you focus your revision effectively.
""")

# Button to trigger search explicitly (Streamlit also re-runs on widget changes)
if st.button("Generate Questions"): # NEW: Changed button text
    st.session_state.search_triggered = True

# Initialize search_triggered state if not present
if 'search_triggered' not in st.session_state:
    st.session_state.search_triggered = False

if st.session_state.search_triggered:
    st.header("Generated Questions")

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
        st.success(f"Found {len(filtered_documents)} question(s) matching your criteria:")
        for i, doc in enumerate(filtered_documents):
            with st.expander(f"**Topic: {doc['topic']} | Level: {doc['level']} | Year: {doc['year']}**"):
                st.markdown(f"**Question {i+1}:**") # Add a question number
                st.write(doc["content"])
                # You could add a download button for each document here if they were actual files
    else:
        st.warning("No questions found matching your selected criteria. Please adjust your filters.")

st.markdown("---")
st.info("💡 Tip: Adjust filters in the sidebar and click 'Generate Questions' to refresh the results.")
