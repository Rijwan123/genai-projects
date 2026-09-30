# check ollama exist- ollama list and replace model in code
#pip install ollama
# https://www.promptingguide.ai/
import ollama

# Change this to your model name if different
MODEL_NAME = "llama3.2:latest"

# 1. Zero-Shot Prompting
def zero_shot_prompt(input_text):
    prompt = f"Summarize the following text:\n{input_text}"
    response = ollama.chat(model=MODEL_NAME, 
                           messages=[{"role": "user", "content": prompt}])
    return response['message']['content']
    #return response

# 2. One-Shot Prompting
def one_shot_prompt(input_text):
    prompt = (
        "Text: The Great Wall of China is one of the Seven Wonders of the World.\n"
        "Summary: The Great Wall of China is a famous Wonder of the World.\n\n"
        f"Text: {input_text}\nSummary:"
    )
    response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# 3. Few-Shot Prompting
def few_shot_prompt(input_text):
    prompt = (
        "Text: The Taj Mahal is a white marble mausoleum in India.\n"
        "Summary: The Taj Mahal is a white marble tomb located in India.\n\n"
        "Text: Mount Everest is the highest mountain above sea level.\n"
        "Summary: Mount Everest is the tallest mountain on Earth.\n\n"
        "Text: The Great Barrier Reef is the largest coral reef system.\n"
        "Summary: The Great Barrier Reef is the world's largest coral reef system.\n\n"
        f"Text: {input_text}\nSummary:"
    )
    response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# 4. Chain-of-Thought Prompting
def chain_of_thought_prompt(input_text):
    prompt = (
        f"Let's think step by step to summarize the following text:\n\n"
        f"Text: {input_text}\n\n"
        "Step 1: Identify the main subject of the sentence.\n"
        "Step 2: Understand what is being said about the subject.\n"
        "Step 3: Combine the subject and key information into one concise sentence.\n"
        "Final Summary:"
    )
    response = ollama.chat(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
    return response['message']['content']


# --- Example Usage ---
if __name__ == "__main__":
    input_text = """Drishyam 3: The Past Never Stays Silent, or simply Drishyam 3, is a 2026 Indian Malayalam-language crime drama film written and directed by Jeethu Joseph. Produced by Antony Perumbavoor for Aashirvad Cinemas, it is a sequel to Drishyam 2 (2021) and the third installment in the Drishyam film series. The film stars Mohanlal, alongside Meena, Ansiba Hassan, Esther Anil, Kalabhavan Shajon, Siddique, Murali Gopy, and Asha Sharath.

Principal photography commenced on 22 September 2025, and concluded on 2 December 2025. The film was released on 21 May 2026 and received mixed reviews from critics. Nonetheless, it emerged as a commercial success, grossing ₹237.70 crore to become the highest-grossing installment in the franchise and one of the highest-grossing Malayalam films ever made.[3] A Hindi remake titled Drishyam: The Conclusion is scheduled to release on 2 October 2026.
"""

    print("=== Zero-Shot ===")
    print(zero_shot_prompt(input_text), "\n")

    print("=== One-Shot ===")
    print(one_shot_prompt(input_text), "\n")

    print("=== Few-Shot ===")
    print(few_shot_prompt(input_text), "\n")

    print("=== Chain of Thought ===")
    print(chain_of_thought_prompt(input_text), "\n")
