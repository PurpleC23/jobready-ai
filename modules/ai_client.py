import ollama

def ask_mistral(prompt: str, system: str = "") -> str:
    """Send a prompt to Mistral and get a response."""
    
    messages = []
    
    if system:
        messages.append({"role": "system", "content": system})
    
    messages.append({"role": "user", "content": prompt})
    
    response = ollama.chat(
        model="mistral",
        messages=messages
    )
    
    return response["message"]["content"]