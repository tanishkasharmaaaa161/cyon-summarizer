import streamlit as st
import os
from llm_core import LLMCore
from prompt_compiler import compile_prompt

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Choose-Your-Own-News Summarizer (CYON-S)",
    layout="wide"
)

# --- INITIALIZATION ---
# Initialize the LLM Core (this handles the API calls)
@st.cache_resource
def initialize_llm():
    # st.secrets automatically reads the openai_api_key from .streamlit/secrets.toml
    api_key = st.secrets["openai_api_key"] 
    return LLMCore(api_key=api_key)

llm_core = initialize_llm()

# Cache the prompt files for quick access
@st.cache_data
def load_prompts(prompt_dir="prompts"):
    prompts = {}
    for filename in os.listdir(prompt_dir):
        if filename.endswith(".txt"):
            key = filename.replace(".txt", "")
            with open(os.path.join(prompt_dir, filename), 'r') as f:
                prompts[key] = f.read()
    return prompts

MANIFESTOS = load_prompts()

# --- SIDEBAR: USER CONTROLS ---

st.sidebar.title("📚 Summary Controls")
st.sidebar.markdown("---")

# 1. Choose Summarization Style (Style Radio Buttons)
style = st.sidebar.radio(
    "Choose Summarization Style:",
    options=["Sherlock", "Policy", "Critic"],
    key="style_selection",
    index=0,
    help="Select the persona and objective for the summarizer."
)

st.sidebar.markdown("---")

# 2. Controllability Sliders
st.sidebar.subheader("Adjust Controllability")

compression_level = st.sidebar.slider(
    "Compression Level (Length)",
    min_value=0.1, max_value=1.0, value=0.6, step=0.05,
    help="Lower value means a shorter, more compressed summary."
)

bias_avoidance = st.sidebar.slider(
    "Bias Avoidance Level (Tone)",
    min_value=0.0, max_value=1.0, value=0.7, step=0.05,
    help="Higher value instructs the model to strictly avoid political or emotional bias."
)

st.sidebar.markdown("---")
st.sidebar.info("Manifestos loaded: " + ", ".join(MANIFESTOS.keys()))


# --- MAIN APPLICATION VIEW ---

st.title("📌 Choose-Your-Own-News Summarizer (CYON-S)")
st.caption("A multi-faceted LLM application featuring style control and prompt-level controllability.")
st.markdown("---")

# Input Field
news_article = st.text_area(
    "Paste the News Article or Text Here:",
    height=300,
    placeholder="Paste a long news article to be summarized..."
)

if st.button("Generate Controlled Summary", type="primary"):
    if not news_article:
        st.warning("Please paste an article to begin summarization.")
    else:
        # --- 1. COMPILE FINAL PROMPT ---
        # The prompt_compiler combines the selected style manifesto with the user's article and sliders.
        with st.spinner("Compiling prompt and fetching summary..."):
            
            # Select the correct manifesto based on the radio button
            style_manifesto = MANIFESTOS.get(style.lower(), MANIFESTOS['sherlock']) 
            
            final_prompt = compile_prompt(
                manifesto=style_manifesto,
                article=news_article,
                compression_level=compression_level,
                bias_avoidance=bias_avoidance
            )
            
            # --- 2. GENERATE SUMMARY ---
            summary_response = llm_core.generate_summary(final_prompt)
            
            # --- 3. RUN HEURISTIC REVIEW ---
            # This module performs prompt-based, heuristic analysis of coherence,
            # length adequacy, and tone neutrality. It does NOT perform factual verification.
            lce_output = llm_core.run_heuristic_review(summary_response)
            
            st.success("Summary Generated Successfully!")

        # --- 4. DISPLAY RESULTS ---
        
        # Use tabs for a clean presentation
        tab1, tab2, tab3 = st.tabs(["Summary Output", "Factuality & Logic Check", "Controllability Insights"])

        with tab1:
            st.header(f"Summary ({style} Style)")
            st.info(f"Generated using **{style}** style with Compression={compression_level} and Bias Avoidance={bias_avoidance}")
            st.write(summary_response)

        with tab2:
            st.header("Heuristic Logic & Tone Review")
            st.code(lce_output)
            st.markdown("""
            *This tab shows the output of a prompt-based heuristic review module that provides indicative signals about logical coherence, summary length adequacy, and tone neutrality.  
            This review is heuristic and does **not** constitute factual verification.*
            """)

        with tab3:
            st.header("Prompt Sent to LLM")
            st.code(final_prompt, language='markdown')
            st.markdown("""
            *This is the complete instruction prompt sent to the OpenAI model, showing how your selected controls (Style, Compression, Bias) translated into specific, detailed instructions.*
            """)