import streamlit as st
import re
import pandas as pd # Import pandas

# --- Data Loading (from CSV) ---
DATA_FILE = "questions.csv"

@st.cache_data # Cache the data loading for better performance
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        # Convert DataFrame rows to a list of dictionaries for easier filtering later
        # Also ensure 'year' is an integer for slider functionality
        documents = df.to_dict(orient='records')
        for doc in documents:
            if 'year' in doc:
                doc['year'] = int(doc['year'])
        return documents
    except FileNotFoundError:
        st.error(f"Error: The data file '{file_path}' was not found. Please ensure it's in the same directory as app.py.")
        return []
    except pd.errors.EmptyDataError:
        st.error(f"Error: The data file '{file_path}' is empty. Please add data to it.")
        return []
    except Exception as e:
        st.error(f"An error occurred while loading the data file: {e}")
        return []

simulated_documents = load_data(DATA_FILE)

# --- Handle case where no data is loaded ---
if not simulated_documents:
    st.warning("No questions loaded. Please check your 'questions.csv' file.")
    st.stop() # Stop the app if no data is available

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
    It identifies inline ($...$) and display ($$...$$) math.
    Inline math is rendered using st.markdown (to keep it inline).
    Display math is rendered using st.latex (as a block).
    """
    # Regex to find display math ($$...$$) and inline math ($...$)
    # The capturing group () around the pattern makes re.split include the delimiters
    pattern = re.compile(r'(\$\$.*?\$\$|\$.*?\$)', re.DOTALL)
    
    # Split the string by the LaTeX patterns, keeping the delimiters in the list
    parts = pattern.split(content_string)
    
    current_markdown_buffer = [] # Buffer to accumulate text and inline math for a single st.markdown call
    
    for part in parts:
        if not part: # Skip any empty strings that might result from split
            continue
            
        if part.startswith('$$') and part.endswith('$$'):
            # If there's content in the markdown buffer, flush it first
            if current_markdown_buffer:
                st.markdown("".join(current_markdown_buffer))
                current_markdown_buffer = [] # Reset buffer
            st.latex(part[2:-2]) # Render display math as a block
        elif part.startswith('$') and part.endswith('$'):
            # Add inline math to the markdown buffer
            current_markdown_buffer.append(part)
        else:
            # Add regular text to the markdown buffer
            current_markdown_buffer.append(part)
            
    # After iterating through all parts, flush any remaining content in the buffer
    if current_markdown_buffer:
        st.markdown("".join(current_markdown_buffer))


# --- Sidebar for Filters ---
st.sidebar.header("Filter Questions")

st.sidebar.subheader("Select Topics")
selected_topics = []
# Dynamic creation of topic checkboxes based on unique topics in the data
unique_topics = sorted(list(set(doc["topic"] for doc in simulated_documents)))
for topic_code in unique_topics:
    # You'll need a mapping for display names if "A", "B", "C" are not descriptive enough
    topic_display_name_map = {
        "A": "Binomial Expansions",
        "B": "Exponential and Logarithmic Functions",
        "C": "Limits",
        "D": "Differentiation and its Application"
    }
    display_name = topic_display_name_map.get(topic_code, f"Topic {topic_code}")
    if st.sidebar.checkbox(display_name, value=(topic_code == "A")): # Default select 'A' for example
        selected_topics.append(topic_code)


st.sidebar.subheader("Select Section")
# This list will now store "A" or "B" directly
selected_sections = []
# Dynamic creation of section checkboxes based on unique sections in the data
unique_sections = sorted(list(set(doc["section"] for doc in simulated_documents)))
for section_code in unique_sections:
    section_display_name = {
        "A": "Section A: Elementary Short Questions",
        "B": "Section B: Long Questions"
    }.get(section_code, f"Section {section_code}")
    if st.sidebar.checkbox(section_display_name, value=(section_code == "A")): # Default select 'A' for example
        selected_sections.append(section_code)


st.sidebar.subheader("Select Years")
# Get the range of years from your loaded data for the slider
min_year = min(doc["year"] for doc in simulated_documents)
max_year = max(doc["year"] for doc in simulated_documents)
selected_years = st.sidebar.slider(
    "Year Range of Questions",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year), # Default to full range
    step=1
)
st.sidebar.info(f"Selected Year Range: **{selected_years[0]} - {selected_years[1]}**")


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
