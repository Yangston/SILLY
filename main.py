import requests
import gradio as gr

# OpenAI API Key
api_key = 'sk-'
catbot = True

# Function to create payload for the ChatGPT API
def create_payload(messages):
    return {
        "model": "gpt-4o",
        "messages": messages,
        "max_tokens": 150,
        "temperature": 0.7
    }

# ChatGPT Function
def chat(message, history):
    # Adding the system message to prime the GPT assistant
    if not history:
        if catbot:
            history = [{"role": "system", "content": "You are a cat person. You love saying 'nyan', 'meow', 'pur', and other cat sounds. You love integrating these sounds into the human language through puns and exclamations."}]
        else: 
            history = [{"role": "system", "content": "You are a cat person. You love saying 'nyan', 'meow', 'pur', and other cat sounds. You love integrating these sounds into the human language through puns and exclamations."},
                        {"role": "user", "content": "Please retype my messages in your cat person language!"}]    
    history.append({"role": "user", "content": message})

    # Create the payload
    payload = create_payload(history)

    # Set headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Make the request to the ChatGPT API
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_data = response.json()

    # Get the assistant's reply
    reply = response_data['choices'][0]['message']['content']

    history.append({"role": "assistant", "content": reply})

    return reply, history

# Gradio Interface Setup
def chatbot_interface(user_input, state):
    reply, state = chat(user_input, state)
    return reply, state

with gr.Blocks() as demo:
    state = gr.State([])

    with gr.Row():
        with gr.Column(scale=6):
            user_input = gr.Textbox(show_label=False, placeholder="Type your message here...")
        
        with gr.Column(scale=1, min_width=100):
            submit_button = gr.Button("Send")

    chatbot_output = gr.Textbox(label="CatBot's Response")

    submit_button.click(fn=chatbot_interface, inputs=[user_input, state], outputs=[chatbot_output, state])

demo.launch()
