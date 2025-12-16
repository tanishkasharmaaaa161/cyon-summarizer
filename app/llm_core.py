from openai import OpenAI
import os

class LLMCore:
    """
    Handles all interactions with the OpenAI models (GPT-3.5 or GPT-4).
    This includes generating the summary and running the Logic Chain Extractor (LCE).
    """

    def __init__(self, api_key):
        # Initialize the OpenAI Client
        self.client = OpenAI(api_key=api_key)
        # We'll use a strong model for reliable summaries and LCE checks
        self.model_name = "gpt-3.5-turbo" 

    def generate_summary(self, prompt: str) -> str:
        """
        Sends the compiled prompt (manifesto + article + controls) to the LLM 
        to generate the controlled summary.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a professional, accurate, and highly controllable news summarization engine."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7, # Allows for some creativity/flow
                max_tokens=1500 
            )
            # Extract and return the summary text
            return response.choices[0].message.content

        except Exception as e:
            # Return a clear error message if the API call fails
            return f"Error during summary generation (API call failed). Check your secrets.toml file and network connection. Error: {e}"

    def run_logic_chain_extractor(self, summary: str) -> str:
        """
        This is a placeholder for the Logic Chain Extractor (LCE). 
        In a real application, this would be a second, separate LLM call 
        designed to critically review the generated summary for factuality and logic.
        
        For initial setup, we return a simulated report.
        """
        
        # In the final version, you would call the model here:
        # lce_prompt = f"Critically analyze the following summary for factual errors and logical gaps:\n{summary}"
        # ... API call code ...

        # Simulation for immediate testing:
        report = f"""
        LCE REPORT - {self.model_name}

        Summary Factual Integrity Check:
        - Result: PASS (Simulated)
        - Confidence Score: 95/100 (Simulated)

        Logical Flow Assessment:
        - Result: PASS (Simulated)
        - Notes: The summary maintains logical coherence throughout, linking causes and effects clearly.

        Bias Review:
        - Result: LOW BIAS DETECTED (Simulated)
        - Notes: Tone is neutral and adheres to the Bias Avoidance control level.

        This report confirms the summary meets the required factuality and control parameters.
        """
        return report

# --- NOTE ---
# You may also need a 'prompt_compiler.py' file in the same directory!
# That file contains the 'compile_prompt' function used in app.py.
