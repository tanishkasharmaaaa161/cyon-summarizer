from openai import OpenAI
import os

class LLMCore:
    """
    Handles interactions with the OpenAI model for prompt-based
    news summarization and heuristic controllability analysis.
    """

    def __init__(self, api_key):
        # Initialize the OpenAI Client
        self.client = OpenAI(api_key=api_key)
        # Model used for prompt-driven news summarization
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

    def run_heuristic_review(self, summary: str) -> str:
        """
        Heuristic review module for logical coherence, length adequacy,
        and tone neutrality. This module does NOT perform factual verification.
        """

        words = summary.split()
        word_count = len(words)

        # Heuristic 1: Length adequacy
        if word_count < 50:
            length_assessment = "Too short – risk of oversimplification"
        elif word_count > 300:
            length_assessment = "Too long – risk of redundancy"
        else:
            length_assessment = "Appropriate compression level"

        # Heuristic 2: Logical flow proxy
        transition_words = ["because", "therefore", "however", "while", "thus", "although"]
        transition_count = sum(1 for w in transition_words if w in summary.lower())

        if transition_count >= 2:
            coherence = "High (clear logical transitions detected)"
        elif transition_count == 1:
            coherence = "Moderate (limited logical transitions)"
        else:
            coherence = "Low (implicit or missing logical connectors)"

        # Heuristic 3: Tone & bias proxy
        opinion_words = ["should", "must", "clearly", "obviously", "undoubtedly"]
        bias_hits = sum(1 for w in opinion_words if w in summary.lower())

        if bias_hits == 0:
            bias_risk = "Low"
        elif bias_hits <= 2:
            bias_risk = "Moderate"
        else:
            bias_risk = "High"

        report = f"""
        HEURISTIC REVIEW REPORT (Prompt-based)

        Length Assessment:
        - {length_assessment}
        - Word Count: {word_count}

        Logical Coherence Indicator:
        - Estimated Level: {coherence}
        - Basis: Transition word analysis

        Tone & Bias Indicator:
        - Estimated Bias Risk: {bias_risk}
        - Basis: Presence of directive or opinionated language

        Disclaimer:
        This review provides heuristic indicators only.
        It does NOT constitute factual verification.
        """

        return report
    