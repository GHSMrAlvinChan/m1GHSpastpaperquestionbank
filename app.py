import streamlit as st
import os # Import os for file system operations

# --- Streamlit App Configuration (MUST BE THE FIRST STREAMLIT COMMAND) ---
st.set_page_config(
    page_title="📚 M1 Past Paper Questions Generator 📊",
    layout="wide",
    initial_sidebar_state="expanded" # Keep sidebar expanded by default
)

# --- Data Folders ---
IMAGE_FOLDER = "images/"    # Folder for question images
SOLUTIONS_FOLDER = "solutions/" # Folder for solution images

@st.cache_data # Cache the data loading for better performance
def load_data_from_images(image_folder, solutions_folder):
    print(f"Attempting to load data from images in: {image_folder}")
    documents = []
    
    if not os.path.exists(image_folder):
        st.error(f"**Error: Question image folder '{image_folder}' not found.**")
        st.markdown("Please ensure the `images/` folder exists in the same directory as your `app.py`.")
        return []

    # Check for solutions folder existence, but don't error out if it's missing (solutions might be optional)
    if not os.path.exists(solutions_folder):
        print(f"Warning: Solution image folder '{solutions_folder}' not found. Solutions will not be loaded.")
        
    try:
        # List all files in the question image folder
        image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
        print(f"Found {len(image_files)} question image files.")

        if not image_files:
            st.warning(f"No image files found in '{image_folder}'. Please upload your question images.")
            return []

        for filename in image_files:
            try:
                # Expected question filename format: Topic_Section_Year_Code.png
                # Example: A_C_2025_S4FinalQ4.png
                
                # Extract filename without extension for parsing
                name_without_ext = os.path.splitext(filename)[0]
                
                parts = name_without_ext.split('_')
                
                topic = ""
                section = ""
                year = None
                code = ""

                if len(parts) >= 3: 
                    topic = parts[0]
                    section = parts[1]
                    try:
                        year = int(parts[2])
                    except ValueError:
                        print(f"Warning: Invalid year '{parts[2]}' in filename: {filename}. Skipping.")
                        continue # Skip this file if year is not an integer

                    if len(parts) >= 4: # If code part exists
                        code = parts[3]
                    # If len(parts) is exactly 3, code remains an empty string as initialized.
                else:
                    print(f"Skipping malformed filename: {filename} (does not match Topic_Section_Year_Code.png or Topic_Section_Year.png format)")
                    continue # Skip malformed filenames

                question_image_url = os.path.join(image_folder, filename)
                
                # Derive solution image path based on the NEW convention: YEAR_CODE.png
                solution_image_url = None
                if year is not None and code: # Only look for a solution if year and code exist
                    solution_filename = f"{year}_{code}.png" # NEW: Year_Code.png
                    potential_solution_path = os.path.join(solutions_folder, solution_filename)
                    if os.path.exists(potential_solution_path):
                        solution_image_url = potential_solution_path
                        print(f"Found solution for {year}-{code}: {solution_image_url}")
                    else:
                        print(f"Solution for {year}-{code} not found at: {potential_solution_path}")

                documents.append({
                    "topic": topic,
                    "section": section,
                    "year": year,
                    "code": code,
                    "image_url": question_image_url,
                    "solution_image_url": solution_image_url # Store the solution image URL (or None)
                })
            except Exception as e:
                print(f"Error processing filename {filename}: {e}. Skipping.")
                continue # Continue to next file on error
        
        print(f"Data loaded from images and parsed successfully. Total questions: {len(documents)}")
        return documents
    except Exception as e:
        st.error(f"An unexpected error occurred while loading images: {e}")
        return []

simulated_documents = load_data_from_images(IMAGE_FOLDER, SOLUTIONS_FOLDER)

# --- Handle case where no data is loaded (after image parsing) ---
if not simulated_documents:
    st.warning("No questions loaded from images. Please ensure images are in the correct folder and named according to the `Topic_Section_Year_Code.png` format.")
    st.stop() # Stop the app if no data is available


# --- Sidebar for Filters ---
st.sidebar.header("Filter Questions")

# --- Topic Display Name Mapping ---
TOPIC_DISPLAY_NAME_MAP = {
    "A": "Binomial Expansions",
    "B": "Exponential and Logarithmic Functions",
    "C": "Limits",
    "D": "Differentiation and its Application",
    "E": "Integration and its Application",
}

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
    display_name = TOPIC_DISPLAY_NAME_MAP.get(topic_code, f"Topic {topic_code}") # Use the map
    
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

# Initialize sorting preference
if 'sort_by_preference' not in st.session_state:
    st.session_state.sort_by_preference = 'year' # Default primary sort

# Create columns for the "Generate Questions" button and sorting radio buttons
btn_generate_col, radio_col_1, radio_col_2, radio_col_3 = st.columns([0.25, 0.25, 0.25, 0.25])

with btn_generate_col:
    if st.button("Generate Questions"):
        st.session_state.search_triggered = True

if 'search_triggered' not in st.session_state:
    st.session_state.search_triggered = False

if st.session_state.search_triggered:
    st.header("Generated Questions")

    # Radio buttons for sorting preference, placed below the "Generated Questions" header
    # Ensure to use a unique key for the radio buttons
    st.session_state.sort_by_preference = st.radio(
        "Sort questions primarily by:",
        ('Year', 'Topic', 'Section'),
        index=('Year', 'Topic', 'Section').index(st.session_state.sort_by_preference.capitalize()), # Set initial value from session state
        key='sort_radio_buttons',
        horizontal=True # Display horizontally to make them closer
    ).lower() # Convert back to lowercase for internal use

    filtered_documents = []
    for doc in simulated_documents:
        topic_match = doc["topic"] in selected_topics
        section_match = doc["section"] in selected_sections
        year_match = selected_years[0] <= doc["year"] <= selected_years[1]

        if topic_match and section_match and year_match:
            filtered_documents.append(doc)

    # --- Dynamic Sorting Logic based on preference ---
    if st.session_state.sort_by_preference == 'year':
        filtered_documents.sort(key=lambda doc: (-doc['year'], doc['topic'], doc['section']))
    elif st.session_state.sort_by_preference == 'topic':
        filtered_documents.sort(key=lambda doc: (doc['topic'], -doc['year'], doc['section']))
    elif st.session_state.sort_by_preference == 'section':
        filtered_documents.sort(key=lambda doc: (doc['section'], -doc['year'], doc['topic']))


    if filtered_documents:
        st.success(f"Found {len(filtered_documents)} question(s) matching your criteria:")
        for i, doc in enumerate(filtered_documents):
            # Get the display name for the topic
            display_topic_name = TOPIC_DISPLAY_NAME_MAP.get(doc['topic'], doc['topic'])
            
            # --- Outer Expander: For the Question ---
            # Initialize a unique session state key for each question's solution visibility
            solution_button_key = f"show_solution_{doc['code']}_{doc['year']}_{doc['topic']}_{doc['section']}"
            if solution_button_key not in st.session_state:
                st.session_state[solution_button_key] = False

            with st.expander(f"**Topic: {display_topic_name} | Section: {doc['section']} | Year: {doc['year']}**"):
                st.markdown(f"**Question {i+1}:**")
                # Use st.columns to control image width and center it
                col_left_padding, col_image, col_right_padding = st.columns([0.15, 0.7, 0.15]) 
                with col_image:
                    # Caption is Year - Code
                    st.image(doc['image_url'], caption=f"{doc['year']} - {doc['code']}", use_container_width=True)

                # --- "Show Solution" Button ---
                # Callback function to toggle the session state
                def _toggle_solution_visibility(key):
                    st.session_state[key] = not st.session_state[key]

                # Determine button label based on current state (before this button click is processed)
                current_solution_visible = st.session_state.get(solution_button_key, False)
                button_label = "Hide Solution" if current_solution_visible else "Show Solution"
                
                # Render the button with the on_click callback
                st.button(button_label, key=f"solution_btn_{doc['code']}_{i}", on_click=_toggle_solution_visibility, args=(solution_button_key,))

                # --- Solution Display Area ---
                if st.session_state[solution_button_key]:
                    st.markdown("### Solution:")
                    if doc['solution_image_url']:
                        # Solution image: Use st.columns to control width and center it
                        sol_col_left, sol_col_image, sol_col_right = st.columns([0.2, 0.6, 0.2])
                        with sol_col_image:
                            st.image(doc['solution_image_url'], caption=f"Solution for {doc['year']} - {doc['code']}", use_container_width=True)
                    else:
                        st.info("Solution is not yet ready for this question.")
    else:
        st.warning("No questions found matching your selected criteria. Please adjust your filters.")

st.markdown("---")
st.info("💡 Tip: Adjust filters in the sidebar and click 'Generate Questions' to refresh the results.")
