import streamlit as st
import re

# --- Simulated Data (Replace with actual file loading if needed for deployment) ---
# In a real scenario, you might load these from a database, a structured file (CSV/JSON),
# or dynamically read from specific .txt files based on a naming convention.
# For this example, we'll use an in-memory list of dictionaries.

# Each dictionary represents a 'document' or 'text file' with its associated metadata
simulated_documents = [
    {"topic": "A", "section": "A", "year": 2020, "content": "Question 1: Derive the equations of motion for a particle under constant acceleration. (Topic A, Section A, 2020)"},
    {"topic": "A", "section": "B", "year": 2021, "content": "Question 2: A block of mass 'm' is pulled along a rough horizontal surface by a force 'F' at an angle 'theta' to the horizontal. Calculate the acceleration of the block. (Topic A, Section B, 2021)"},
    {"topic": "A", "section": "B", "year": 2022, "content": "Question 3: A particle moves in a straight line such that its velocity 'v' at time 't' is given by v = 3t^2 - 6t. Find the total distance travelled by the particle in the first 3 seconds. (Topic A, Section B, 2022)"},
    {"topic": "B", "section": "A", "year": 2019, "content": "Question 4: State Newton's three laws of motion. (Topic B, Section A, 2019)"},
    {"topic": "B", "section": "B", "year": 2020, "content": "Question 5: A force of (3i + 4j) N acts on a particle. Find the magnitude of this force. (Topic B, Section B, 2020)"},
    {"topic": "B", "section": "B", "year": 2023, "content": "Question 6: Two particles, P and Q, are moving towards each other along a straight line. Given their initial velocities and the coefficient of restitution, calculate their velocities after impact. (Topic B, Section B, 2023)"},
    {"topic": "C", "section": "A", "year": 2021, "content": "Question 7: Define momentum and impulse. (Topic C, Section A, 2021)"},
    {"topic": "C", "section": "B", "year": 2022, "content": "Question 8: A bullet of mass 'm' is fired into a block of mass 'M' which is initially at rest. The bullet becomes embedded in the block. Calculate the common velocity of the bullet and block immediately after impact. (Topic C, Section B, 2022)"},
    {"topic": "C", "section": "B", "year": 2024, "content": "Question 9: A car of mass 1200 kg is travelling up a hill inclined at an angle 'alpha' to the horizontal. The engine produces a constant power P. Given the resistance to motion, find the maximum speed the car can attain. (Topic C, Section B, 2024)"},
    {"topic": "A", "section": "A", "year": 2021, "content": "Question 10: Illustrate the difference between speed and velocity with examples. (Topic A, Section A, 2021)"},
    {"topic": "B", "section": "A", "year": 2021, "content": "Question 11: Explain the concept of weightlessness in orbit. (Topic B, Section A, 2021)"},
    {"topic": "C", "section": "B", "year": 2023, "content": "Question 12: A ball is thrown vertically upwards from the ground with an initial speed of U m/s. Find the time taken to reach its maximum height. (Topic C, Section B, 2023)"},
    {"topic": "D", "section": "A", "year": 2021, "content": "This is a trial question."},
    # Document with LaTeX content, demonstrating both inline and display math
    {"topic": "A", "section": "B", "year": 2025, "content": "Question 13: Consider a particle moving with velocity $v(t) = 2t + 3$. Find its acceleration at $t=2$ seconds. Also, calculate the displacement from $t=0$ to $t=4$ using the integral: $$ s = \\int_0^4 (2t + 3) dt $$ The final answer should be $s = 28$ units. (Topic A, Section B, 2025)"}
]

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="📚 M1 Past Paper Questions Generator 📊",
    layout="wide",
    initial_sidebar_state="expanded" # Keep sidebar expanded by default
)

# --- Helper function to render content with LaTeX ---
def render_content_with_latex(content_string):
    """
    Renders a string containing mixed text and LaTeX.
    It identifies inline ($...$) and display ($$...$$) math and uses st.markdown for inline
    and st.latex for display.
    """
    # Regex to find display math ($$...$$) and inline math ($...$)
    # Prioritize display math to avoid issues if $$ is part of inline regex match
    latex_patterns = re.compile(r'(\$\$.*?\$\$|\$.*?\$)', re.DOTALL)
    
    parts = latex_patterns.split(content_string)
    
    for part in parts:
        if part.startswith('$$') and part.endswith('$$'):
            st.latex(part[2:-2]) # Remove $$ delimiters for st.latex (block math)
        elif part.startswith('$') and part.endswith('$'):
            st.markdown(part) # Keep $ delimiters for st.markdown (inline math)
        else:
            st.markdown(part) # Regular text


# --- Sidebar for Filters ---
st.sidebar.header("Filter Questions")

st.sidebar.subheader("Select Topics")
selected_topics = []
if st.sidebar.checkbox("Binomial Expansions", value=True): # Default selected
    selected_topics.append("A")
if st.sidebar.checkbox("Exponential and Logarithmic Functions"):
    selected_topics.append("B")
if st.sidebar.checkbox("Limits"):
    selected_topics.append("C")
if st.sidebar.checkbox("Differentiation and its Application"):
    selected_topics.append("D")

st.sidebar.subheader("Select Section")
# This list will now store "A" or "B" directly
selected_sections = []
if st.sidebar.checkbox("Section A: Elementary Short Questions", value=True): # Default selected
    selected_sections.append("A")
if st.sidebar.checkbox("Section B: Long Questions"):
    selected_sections.append("B")

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
st.title("📚 M1 Past Paper Questions Generator 📊")
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

        # Check if section matches
        section_match = doc["section"] in selected_sections

        # Check if year is within the selected range
        year_match = selected_years[0] <= doc["year"] <= selected_years[1]

        if topic_match and section_match and year_match:
            filtered_documents.append(doc)

    # --- Display Results ---
    if filtered_documents:
        st.success(f"Found {len(filtered_documents)} question(s) matching your criteria:")
        for i, doc in enumerate(filtered_documents):
            # Display section directly from doc["section"]
            with st.expander(f"**Topic: {doc['topic']} | Section: {doc['section']} | Year: {doc['year']}**"):
                st.markdown(f"**Question {i+1}:**")
                # Call the new rendering function
                render_content_with_latex(doc["content"])
    else:
        st.warning("No questions found matching your selected criteria. Please adjust your filters.")

st.markdown("---")
st.info("💡 Tip: Adjust filters in the sidebar and click 'Generate Questions' to refresh the results.")
