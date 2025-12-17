# Choose-Your-Own-News Summarizer (CYON-S)

CYON-S is a prompt-driven GenAI application that enables users to generate controllable news summaries using different stylistic personas and explicit prompt-level controls.  
The project is developed as part of the Advanced NLP (AINLP) coursework and emphasizes prompt engineering, controllability, and human-centered evaluation, with zero model training.

---

## Project Objective

The objective of CYON-S is to demonstrate how large language models can be controlled through structured prompts rather than model fine-tuning.  
The system exposes interpretable controls such as summary style, compression level, and bias avoidance, which are translated into explicit instructions sent to the LLM.

---

## Key Features

### 1. Multiple Summary Styles (Personas)

The system supports three distinct summarization personas implemented entirely through prompt engineering:

- **Sherlock** – logical, deductive, and analytical
- **Policy Analyst** – neutral, policy-focused, and impact-oriented
- **Media Critic** – critical of rhetoric, framing, and power structures

Each persona represents a different interpretive lens over the same news content.

---

### 2. Prompt-Level Controllability

Users can adjust two explicit controls:

- **Compression Level (Length)** – controls how detailed or concise the summary should be
- **Bias Avoidance Level (Tone)** – controls how strongly the model is instructed to avoid subjective or emotional language

Numeric control values are converted into human-readable instructions and embedded directly into the prompt.

---

### 3. Heuristic Logic and Tone Review

The system includes a heuristic review module that provides indicative signals about:

- summary length adequacy
- logical coherence (based on transition cues)
- tone and bias risk (based on directive or opinionated language)

This module is intended for interpretability and controllability analysis.

**Note:**  
This review is heuristic and prompt-based. It does not perform factual verification or ground-truth validation.

---

### 4. Prompt Transparency

The complete instruction prompt sent to the LLM is displayed in the user interface.  
This allows evaluators to inspect how persona selection and control parameters influence the model’s behavior.

---

## System Architecture (High Level)

User Input (News Article)  
→ Style Selection and Control Sliders  
→ Prompt Compilation (Structured Instructions)  
→ LLM Summary Generation  
→ Heuristic Review (Interpretability Layer)  
→ UI Output with Prompt Transparency

---

## Technology Stack

- Frontend / UI: Streamlit  
- LLM API: OpenAI (GPT-3.5 Turbo)  
- Core Logic: Python  
- Deployment: Streamlit-compatible setup  
- Model Training: None (prompt-based only)

---

## Repository Structure

├── app/
│ ├── app.py # Streamlit application
│ ├── llm_core.py # LLM interaction and heuristic review
│ └── prompt_compiler.py # Prompt construction logic
├── prompts/
│ └── *.txt # Style manifestos
├── requirements.txt
├── README.md
└── .gitignore

---

## API Key Setup (Local)

The application expects the OpenAI API key to be provided via Streamlit secrets.

Create the following file locally (do not commit this file):

`.streamlit/secrets.toml`

Add the key in the following format:

`openai_api_key = "your-api-key-here"`


---

## Running the Application Locally

```bash
pip install -r requirements.txt
streamlit run app/app.py
```

The application will be available at:

http://localhost:8501

---

## Evaluation Approach

The system is evaluated using human evaluation, focusing on:

- clarity of generated summaries
- perceived usefulness of different styles
- effectiveness of controllability parameters

This approach aligns with the project’s emphasis on human-perceived quality rather than automated evaluation metrics.

---

## Limitations and Ethical Considerations

- The system does not verify factual correctness of generated summaries.
- Outputs may reflect biases present in the model’s training data despite bias-avoidance instructions.
- Critical or interpretive personas intentionally introduce subjective perspectives.
- Generated summaries should not be treated as authoritative sources.

---

## Academic Note

This project intentionally prioritizes prompt engineering, controllability, interpretability, and deployment realism over model training or automated verification pipelines, in line with the course objectives.

---

## Team

This project was developed collaboratively as part of a group assignment, with contributions across system design, prompt engineering, UI development, deployment, evaluation, and ethics analysis.
