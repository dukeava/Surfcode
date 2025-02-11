import streamlit as st
import openai  #  Add OpenAI for API calls
import time
import matplotlib.pyplot as plt
import ast

# 🔑 Set OpenAI API Key (Replace with your actual API key)
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

client = openai.OpenAI(api_key=OPENAI_API_KEY)

openai.api_key = OPENAI_API_KEY



# Force Streamlit to Use Urbanist Font & Full Dark Mode
st.markdown(
    """
    <style>
        /* Import Urbanist Font */
        @import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@100..900&display=swap');

        /* Apply Urbanist Font to EVERYTHING */
        html, body, [class*="st"], [data-testid] {
            font-family: 'Urbanist', sans-serif !important;
            color: white !important;  /* Force all text to be white */
        }

        /* REMOVE WHITE BAR (Make it Black) */
        [data-testid="stHeader"] {
            background-color: #000000 !important;
        }

        /* Fix Page Background */
        [data-testid="stToolbar"] {
            visibility: hidden !important;
        }
        /* FADE-IN ANIMATION */
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        /* Force full-page background to black */
        [data-testid="stAppViewContainer"] {
            background-color: #000000 !important;
        }

        /* Make sidebar dark */
        [data-testid="stSidebar"] {
            background-color: #121212 !important;
        }

        /* CENTER ALL CONTENT */
        .main-container {
            text-align: center;
        }

        /* Fix Buttons */
        button {
            background-color: #333 !important;
            color: white !important;
            border: none !important;
            font-family: 'Urbanist', sans-serif !important;
            
            
        }
          /* 🔥 Fully Center the Button */
        .stButton {
            display: flex;
            justify-content: center; /* Center horizontally */
            align-items: center;
        }

        .stButton > button {
            width: fit-content; /* Keep button size dynamic */
            padding: 10px 20px; /* Adjust padding */
        }

        /* Force Subheaders, Paragraphs, and Labels to be White */
        h1, h2, h3, h4, h5, h6, p, label, span {
            color: white !important;
            font-family: 'Urbanist', sans-serif !important;
        }

        /* Gradient Header with Fixed Font Size */
        .gradient-text {
            font-size: 72px !important; /* Make it Big */
            font-weight: bold;
            background: linear-gradient(to right, #00A6FF, #FF00FF, #FFD700);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            font-family: 'Urbanist', sans-serif !important;
            line-height: 1.2; /* Fix spacing */
            margin-bottom: 20px;
        }
          /* Fix Code Block Background (Make it Dark) */
        textarea, input {
            background-color: #222222 !important;
            color: white !important;
            
            border-radius: 8px !important;
            padding: 10px !important;
            font-size: 14px !important;
        }

        /* Ensure Streamlit wrapper elements are dark */
        div[data-baseweb="textarea"], div[data-baseweb="input"] {
            background-color: #222222 !important;
            color: white !important;
            border-radius: 8px !important;
            border: 1px solid #FF4444 !important;
        }

         pre, code {
            background-color: #222222 !important;  /* Dark background */
            color: white !important;  /* White text */
            border-radius: 8px !important;
            padding: 10px !important;
            font-size: 14px !important;
            white-space: pre-wrap !important;
            word-wrap: break-word !important;
            overflow-x: auto !important;
        }

        /* 🔥 Fix AI Response Box Wrapper */
        div[data-testid="stCode"] {
            background-color: #222222 !important;  /* Dark response box */
            color: white !important;
            border-radius: 8px !important;
            padding: 10px !important;
            border: 1px solid #FF4444 !important;
        }
         
         .stTextArea textarea {
            white-space: pre-wrap !important;
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
            background-color: #222222 !important; /* Dark Mode */
            color: white !important;
            border-radius: 8px !important;
            font-family: 'Courier New', monospace !important;
        }
         

    

    </style>
    """,
    unsafe_allow_html=True
)

# 🔥 Apply the Gradient Text Using a <p> Instead of <h1>
st.markdown('<p class="gradient-text">Welcome to Surfcode</p>', unsafe_allow_html=True)


# User Input Box
user_input = st.text_area("Enter a coding request (e.g., 'Fix my Python error', 'Generate a Flask app'):")

# Submit Button
if st.button("Generate"):
    if user_input:
        with st.spinner("Generating code..."):
            # 🔥 Send request to OpenAI API
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Using GPT-4
                messages=[{"role": "user", "content": user_input}]
            )
            
            # Extract AI-generated code
            ai_code = response.choices[0].message.content  # ✅ New format (Works!)
            
            # Display AI Response as Code Block
            st.subheader("💡 AI-Generated Code")
            st.text_area("Code Output:", value=ai_code, height=300)
# Function to Calculate Execution Time
def measure_execution_time(code):
    start_time = time.time()
    try:
        exec(code, {}, {})  # Execute the code safely
    except Exception as e:
        return None  # Ignore errors in execution time
    return time.time() - start_time

# Function to Count Lines of Code
def count_lines(code):
    return len(code.strip().split("\n"))

# Function to Estimate Complexity (Basic: Count "if", "for", "while")
def estimate_complexity(code):
    keywords = ["if", "for", "while", "def", "class"]
    return sum(code.count(keyword) for keyword in keywords)

# Only Run Analysis if AI Generated Code
if user_input:
    execution_time = measure_execution_time(ai_code)
    num_lines = count_lines(ai_code)
    complexity = estimate_complexity(ai_code)

    # Define Metrics and Values **INSIDE** the if block
    metrics = ["Execution Time (s)", "Lines of Code", "Complexity Score"]
    values = [execution_time or 0, num_lines, complexity]

    # Matplotlib Chart
    st.subheader("📊 Surfcode Analysis")
    fig, ax = plt.subplots(figsize=(8, 4))

    plt.style.use("dark_background")

    # Create bar chart
    ax.barh(metrics, values, color="#FF4444")  # Neon pink bars

    # Customize the look
    ax.set_xlabel("Efficiency Metrics", color="white")
    ax.set_title("Code Efficiency Analysis", color="white")
    ax.tick_params(axis="both", colors="white")

    # 🔥 Set background to black
    fig.patch.set_facecolor("#000000")  # Overall figure background
    ax.set_facecolor("#121212")  # Chart background

    # Show the figure
    st.pyplot(fig)
