import streamlit as st
import os # Import os for file system operations
import re # Still used for potential string parsing if needed for other features

# --- Streamlit App Configuration (MUST BE THE FIRST STREAMLIT COMMAND) ---
st.set_page_config(
    page_title="📚 M1 Past Paper Questions Generator 📊",
    layout="wide",
    initial_sidebar_state="expanded" # Keep sidebar expanded by default
)

# --- Data Loading (from Image Files) ---
IMAGE_FOLDER = "images/" # Folder where your question images are stored

@st.cache_data # Cache the data loading for better performance
def load_data_from_images(image_folder):
    print(f"Attempting to load data from images in: {image_folder}")
    documents = []
    
    if not os.path.exists(image_folder):
        st.error(f"**Error: Image folder '{image_folder}' not found.**")
        st.markdown("Please ensure the `images/` folder exists in the same directory as your `app.py`.")
        return []

    try:
        # List all files in the image folder
        image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
        print(f"Found {len(image_files)} image files.")

        if not image_files:
            st.warning(f"No image files found in '{image_folder}'. Please upload your question images.")
            return []

        for filename in image_files:
            try:
                # Expected format: Topic_Section_Year_Code.png
                # Example: A_C_2025_S4FinalQ4.png
                parts = filename.split('_')
                if len(parts) >= 3: # Ensure we have at least topic, section, year
                    topic = parts[0]
                    section = parts[1]
                    year = int(parts[2])
                    
                    image_url = os.path.join(image_folder, filename)
                    documents.append({
                        "topic": topic,
                        "section": section,
                        "year": year,
                        "image_url": image_url
                    })
                else:
                    print(f"Skipping malformed filename: {filename} (does not match Topic_Section_Year_Code.png format)")
            except ValueError:
                print(f"Skipping file due to invalid year in filename: {filename}")
            except IndexError:
                print(f"Skipping file due to unexpected filename format: {filename}")
        
        print("Data loaded from images and parsed successfully!")
        return documents
    except Exception as e:
        st.error(f"An unexpected error occurred while loading images: {e}")
        return []

simulated_documents = load_data_from_images(IMAGE_FOLDER)

# --- Handle case where no data is loaded (after image parsing) ---
if not simulated_documents:
    st.warning("No questions loaded from images. Please ensure images are in the correct folder and named according to the `Topic_Section_Year_Code.png` format.")
    st.stop() # Stop the app if no data is available


# --- Helper function to render content (removed as questions are images now) ---
# This function is no longer used for the primary question content (which is now an image).
# Keeping the definition commented out in case you want to revert or use it for other text elements.
# def render_content_with_latex(content_string):
#     processed_content_string = content_string.replace('\\n', '  \n').replace('[NEWLINE]', '  \n')
#     pattern = re.compile(r'(\$\$.*?\$\$|\$.*?\$)', re.DOTALL)
#     parts = pattern.split(processed_content_string) 
#     current_markdown_buffer = [] 
#     for part in parts:
#         if not part: 
#             continue
#         if part.startswith('$$') and part.endswith('$$'):
#             if current_markdown_buffer:
#                 st.markdown("".join(current_markdown_buffer))
#                 current_markdown_buffer = [] 
#             latex_expression = part[2:-2].strip() 
#             latex_expression = latex_expression.replace('\\\\', '\\')
#             latex_expression = latex_expression.replace('\\_', '_')
#             st.latex(latex_expression) 
#         elif part.startswith('$') and part.endswith('$'):
#             current_markdown_buffer.append(part)
#         else:
#             current_markdown_buffer.append(part)
#     if current_markdown_buffer:
#         st.markdown("".join(current_markdown_buffer))


# --- Sidebar for Filters ---
st.sidebar.header("Filter Questions")

st.sidebar.subheader("Topic(s)")
selected_topics = []
# Dynamic creation of topic checkboxes based on unique topics found in image filenames
unique_topics = sorted(list(set(doc["topic"] for doc in simulated_documents)))

# Initialize default topic selections only once
if 'topic_checkbox_states' not in st.session_state:
    # Default select 'A' if it exists, otherwise select the first unique topic
    initial_topic_a_checked = "A" in unique_topics
    st.session_state.topic_checkbox_states = {
        topic_code: (topic_code == "A" if initial_topic_a_checked else (topic_code == unique_topics[0] if unique_topics else False))
        for topic_code in unique_topics
    }
    
for topic_code in unique_topics:
    topic_display_name_map = {
        "A": "Binomial Expansions",
        "B": "Exponential and Logarithmic Functions",
        "C": "Limits",
        "D": "Differentiation and its Application",
        "E": "Integration and its Application",
    }
    display_name = topic_display_name_map.get(topic_code, f"Topic {topic_code}")
    
    checkbox_value = st.sidebar.checkbox(display_name, value=st.session_state.topic_checkbox_states.get(topic_code, False), key=f"topic_cb_{topic_code}")
    st.session_state.topic_checkbox_states[topic_code] = checkbox_value

    if checkbox_value:
        selected_topics.append(topic_code)


st.sidebar.subheader("Section(s)")
selected_sections = []
# Dynamic creation of section checkboxes based on unique sections found in image filenames
unique_sections = sorted(list(set(doc["section"] for doc in simulated_documents)))

# Initialize default section selections only once
if 'section_checkbox_states' not in st.session_state:
    # Default select 'A' if it exists, otherwise select the first unique section
    initial_section_a_checked = "A" in unique_sections
    st.session_state.section_checkbox_states = {
        section_code: (section_code == "A" if initial_section_a_checked else (section_code == unique_sections[0] if unique_sections else False))
        for section_code in unique_sections
    }

for section_code in unique_sections:
    section_display_name = {
        "A": "Section A: Elementary Short Questions",
        "B": "Section B: Long Questions"
    }.get(section_code, f"Section {section_code}")
    
    checkbox_value = st.sidebar.checkbox(section_display_name, value=st.session_state.section_checkbox_states.get(section_code, False), key=f"section_cb_{section_code}")
    st.session_state.section_checkbox_states[section_code] = checkbox_value

    if checkbox_value:
        selected_sections.append(section_code)


st.sidebar.subheader("Year(s)")
# Get the range of years from your loaded data for the slider
min_year = min(doc["year"] for doc in simulated_documents)
max_year = max(doc["year"] for doc in simulated_documents)

# Initialize slider value if not already set, otherwise use existing session state
if 'years_slider_value' not in st.session_state:
    # Default to past 3 years if data supports, otherwise full range
    default_slider_value = (max_year - 2, max_year)
    if (max_year - 2) < min_year:
        default_slider_value = (min_year, max_year)
    st.session_state.years_slider_value = default_slider_value

selected_years = st.sidebar.slider(
    "Range of Years",
    min_value=min_year,
    max_value=max_year,
    value=st.session_state.years_slider_value, # Use session state for persistence
    step=1,
    key="years_slider"
)
st.session_state.years_slider_value = selected_years # Update session state on slider change

st.sidebar.info(f"Selected Year Range: **{selected_years[0]} - {selected_years[1]}**")


# --- Main Content Area ---
st.title("📚 M1 Past Paper Questions Generator 📊")
st.markdown("""
Welcome to the **M1 Past Paper Questions Generator**! Use the filters in the sidebar to dynamically
select and display relevant past paper questions based on specific topics, sections, and
years. This helps you focus your revision effectively.
""")

if st.button("Generate Questions"):
    st.session_state.search_triggered = True

if 'search_triggered' not in st.session_state:
    st.session_state.search_triggered = False

if st.session_state.search_triggered:
    st.header("Generated Questions")

    filtered_documents = []
    for doc in simulated_documents:
        # Check if selected_topics/selected_sections are empty (meaning nothing is checked)
        # If no topics are selected, no topic_match. If no sections are selected, no section_match.
        # This implicitly filters out everything if no checkbox is active.
        topic_match = doc["topic"] in selected_topics
        section_match = doc["section"] in selected_sections
        year_match = selected_years[0] <= doc["year"] <= selected_years[1]

        if topic_match and section_match and year_match:
            filtered_documents.append(doc)

    # --- Sorting Logic ---
    filtered_documents.sort(key=lambda doc: (-doc['year'], doc['topic'], doc['section']))

    if filtered_documents:
        st.success(f"Found {len(filtered_documents)} question(s) matching your criteria:")
        for i, doc in enumerate(filtered_documents):
            with st.expander(f"**Topic: {doc['topic']} | Section: {doc['section']} | Year: {doc['year']}**"):
                st.markdown(f"**Question {i+1}:**")
                # Display the image using st.image
                st.image(doc['image_url'], caption=f"Question {i+1} - {doc['topic']} ({doc['section']}), {doc['year']}", use_column_width=True)
                # Add fallback in case image fails to load (optional, useful for debugging broken links)
                # st.markdown(f"If image above does not load, please check path: `{doc['image_url']}`")
    else:
        st.warning("No questions found matching your selected criteria. Please adjust your filters.")

st.markdown("---")
st.info("💡 Tip: Adjust filters in the sidebar and click 'Generate Questions' to refresh the results.")
