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
    page_title="� M1 Past Paper Questions Generator 📊",
    layout="wide",
    initial_sidebar_state="expanded" # Keep sidebar expanded by default
)

# --- Sidebar for Filters ---
st.sidebar.header("Filter Questions")

# --- Topics Filter ---
# Use columns to place 'Select All Topics' next to the subheader with smaller font
col1_topic_header, col2_topic_select_all = st.sidebar.columns([0.7, 0.3])
col1_topic_header.subheader("Select Topics")
select_all_topics = col2_topic_select_all.checkbox(
    "<small>Select All</small>",
    key="select_all_topics_cb",
    value=st.session_state.get("select_all_topics_cb", False), # Maintain state
    help="Select all available topics",
    unsafe_allow_html=True # Allows rendering <small> tag in label
)

all_possible_topics = ["A", "B", "C"]
selected_topics = []
if select_all_topics:
    selected_topics = all_possible_topics
    st.sidebar.markdown("<small style='color: gray;'>Individual checkboxes are selected when 'Select All' is checked.</small>", unsafe_allow_html=True)
    for topic in all_possible_topics:
        topic_label = f"Topic {topic} ({'Kinematics' if topic == 'A' else 'Forces & Newton\'s Laws' if topic == 'B' else 'Momentum & Energy'})"
        st.sidebar.checkbox(topic_label, value=True, disabled=True, key=f"disabled_topic_cb_{topic}")
else:
    if st.sidebar.checkbox("Topic A (Kinematics)", value=True, key="topic_a_cb"):
        selected_topics.append("A")
    if st.sidebar.checkbox("Topic B (Forces & Newton's Laws)", key="topic_b_cb"):
        selected_topics.append("B")
    if st.sidebar.checkbox("Topic C (Momentum & Energy)", key="topic_c_cb"):
        selected_topics.append("C")

# --- Sections Filter (formerly Levels) ---
# Use columns to place 'Select All Sections' next to the subheader with smaller font
col1_section_header, col2_section_select_all = st.sidebar.columns([0.7, 0.3])
col1_section_header.subheader("Select Section") # Updated subheader
select_all_sections = col2_section_select_all.checkbox(
    "<small>Select All</small>",
    key="select_all_sections_cb",
    value=st.session_state.get("select_all_sections_cb", False), # Maintain state
    help="Select all available sections",
    unsafe_allow_html=True # Allows rendering <small> tag in label
)

all_possible_sections_display = [
    "Section A: Elementary Short Questions", # Updated text
    "Section B: Long Questions"
]
selected_levels_for_filtering = [] # This will store the actual numerical levels (1, 2, 3)
if select_all_sections:
    selected_levels_for_filtering = [1, 2, 3] # Select all levels
    st.sidebar.markdown("<small style='color: gray;'>Individual checkboxes are selected when 'Select All' is checked.</small>", unsafe_allow_html=True)
    st.sidebar.checkbox(all_possible_sections_display[0], value=True, disabled=True, key="disabled_section_a_cb")
    st.sidebar.checkbox(all_possible_sections_display[1], value=True, disabled=True, key="disabled_section_b_cb")
else:
    if st.sidebar.checkbox(all_possible_sections_display[0], value=True, key="section_a_cb"):
        selected_levels_for_filtering.append(1) # Section A corresponds to Level 1
    if st.sidebar.checkbox(all_possible_sections_display[1], key="section_b_cb"):
        selected_levels_for_filtering.extend([2, 3]) # Section B corresponds to Levels 2 and 3


# --- Years Filter ---
st.sidebar.subheader("Select Years") # Removed columns for "Select All Years" checkbox

min_year = min(doc["year"] for doc in simulated_documents)
max_year = max(doc["year"] for doc in simulated_documents)
    
selected_years = st.sidebar.slider(
    "Year Range of Questions",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year), # Default to full range
    step=1,
    key="years_slider",
    disabled=False # Slider is always enabled as "Select All Years" is removed
)

st.sidebar.info(f"Currently selected year range: **{selected_years[0]} - {selected_years[1]}**")


# --- Main Content Area ---
st.title("📚 M1 Past Paper Questions Generator 📊") # Updated main title
st.markdown("""
Welcome to the **M1 Past Paper Questions Generator**! Use the filters in the sidebar to dynamically
select and display relevant past paper questions based on specific topics, sections, and
years. This helps you focus your revision effectively.
""")

# Button to trigger search explicitly (Streamlit also re-runs on widget changes)
if st.button("Generate Questions"):
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

        # Check if level matches the selected sections
        # Now filtering based on `selected_levels_for_filtering`
        level_match = doc["level"] in selected_levels_for_filtering

        # Check if year is within the selected range
        year_match = selected_years[0] <= doc["year"] <= selected_years[1]

        if topic_match and level_match and year_match:
            filtered_documents.append(doc)

    # --- Display Results ---
    if filtered_documents:
        st.success(f"Found {len(filtered_documents)} question(s) matching your criteria:")
        for i, doc in enumerate(filtered_documents):
            # Display level as Section A/B in the expander title for clarity
            display_section = "Section A" if doc["level"] == 1 else "Section B"
            with st.expander(f"**Topic: {doc['topic']} | Section: {display_section} | Year: {doc['year']}**"):
                st.markdown(f"**Question {i+1}:**")
                st.write(doc["content"])
    else:
        st.warning("No questions found matching your selected criteria. Please adjust your filters.")

st.markdown("---")
st.info("💡 Tip: Adjust filters in the sidebar and click 'Generate Questions' to refresh the results.")
