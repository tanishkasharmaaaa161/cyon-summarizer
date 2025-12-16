def compile_prompt(manifesto: str, article: str, compression_level: float, bias_avoidance: float) -> str:
    """
    Compiles the final, comprehensive prompt that is sent to the LLM.
    
    It integrates the selected style manifesto, the user's article, and 
    the numerical control parameters into a single instruction set.
    """
    
    # 1. Convert numerical controls to human-readable instructions
    
    # Compression Level (0.1 = Very Short, 1.0 = Max Length)
    if compression_level >= 0.8:
        length_instruction = "The final summary should be as comprehensive as possible, minimizing compression."
    elif compression_level >= 0.5:
        length_instruction = "The summary should be moderate in length, targeting about 60% of the original article's detail."
    else:
        length_instruction = "The summary must be highly compressed and brief, capturing only the main points."

    # Bias Avoidance (0.0 = Ignore Bias, 1.0 = Strict Neutrality)
    if bias_avoidance >= 0.9:
        bias_instruction = "Crucially, maintain absolute and strict neutrality. Eliminate all emotional, political, or subjective language."
    elif bias_avoidance >= 0.5:
        bias_instruction = "Maintain a neutral tone and remove any obvious political or emotional bias."
    else:
        bias_instruction = "Bias avoidance is a lower priority; focus on summarizing based on the style provided."

    # 2. Assemble the Final Prompt Template
    
    final_prompt = f"""
    --- ROLE AND INSTRUCTIONS ---

    1. **Persona**: Adopt the persona and follow the guidelines defined in the [MANIFESTO].
    2. **Task**: Summarize the provided [ARTICLE] based on the persona and the following control parameters.
    3. **Length Control**: {length_instruction}
    4. **Bias Control**: {bias_instruction}
    5. **Format**: The output must be the final summary text ONLY, with no introductory phrases.

    --- MANIFESTO ---
    {manifesto}

    --- ARTICLE TO SUMMARIZE ---
    {article}
    """
    
    return final_prompt.strip()