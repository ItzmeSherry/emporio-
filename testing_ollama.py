import ollama

def ask_ollama(prompt):
    response = ollama.chat(
        model="qwen3:3b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response["message"]["content"]

answer = ask_ollama("What is the capital of India?")
print(answer)