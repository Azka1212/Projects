import openai
import datetime

# Set up OpenAI API key
openai.api_key = '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'

class UserSession:
    def __init__(self, specialty):
        self.specialty = specialty
        self.chat_history = []  # List to store chat messages

    def add_message(self, message):
        self.chat_history.append(message)

def start_session():
    print("Welcome to the medical chatbot!")
    print("Please select a specialty:")
    print("1. Cardio")
    print("2. Clinical Psychology")
    print("3. Dentistry")
    specialty_choice = input("Enter the number corresponding to your choice: ")
    specialties = {
        '1': 'Cardio',
        '2': 'Clinical Psychology',
        '3': 'Dentistry'
    }
    specialty = specialties.get(specialty_choice)
    if specialty:
        session = UserSession(specialty)
        return session
    else:
        print("Invalid specialty choice.")
        return None 

def get_user_input():
    return input("User: ")

def store_chat_message(session, message):
    session.add_message(message)

def ask_patient_question(question, session):
    print(question)
    user_input = get_user_input()
    store_chat_message(session, {'timestamp': datetime.datetime.now(), 'content': user_input})
    return user_input

def generate_medical_response(chat_history, specialty):
    try:
        if not chat_history:
            # If chat history is empty, return a prompt to start the conversation
            return "Please start the conversation by sharing your concerns."

        # Extract user input from chat history if available
        patient_concern = chat_history[0]['content'] if len(chat_history) > 0 else ""
        trigger = chat_history[1]['content'] if len(chat_history) > 1 else ""
        symptoms_duration = chat_history[2]['content'] if len(chat_history) > 2 else ""
        daily_changes = chat_history[3]['content'] if len(chat_history) > 3 else ""

        # Build the prompt for professional suggestions
        prompt_suggestions = f"""Act as an expert clinical psychiatrist to talk to patients with mental health issues in order to accurately diagnose their problems by performing the following steps one by one: 
1. Greet the patient and introduce yourself as a chatbot trained to help people through their mental health issues 
2. Make it clear that the information shared here will remain confidential 
3. Ask for the patient’s introduction 
4. Get to know the patient by initiating small talk with simple questions like: 
    - How is your day going? 
    - How have you been? 
    - How are you feeling? 
    - Is there anything bothering you? Would you like to share how you are coping with it? 
5. Keep asking questions to dive deeper into your patient’s mental state until the patient has given you enough information for an accurate diagnosis 
6. Once you have a diagnosis, probe the patient with questions to confirm if their symptoms match the mental health issue you have identified. Then, use academic literature and the most credible and updated sources of information in the field of clinical psychiatry to identify and confirm the diagnosis. 
7. As kindly as possible, explain the mental health issue to the patient and answer all the questions they may have regarding their diagnosis before recommending sources like credible textbooks or papers for further reading 
8. Lastly, conduct thorough research on the identified issue to create a comprehensive step-by-step plan for the patient’s treatment, which must include usually prescribed medication and mental and physical exercises to treat the identified issue along with reasoning and evidence from credible sources to support the prescribed steps for treatment 
9. Then, ask the patient if they would like to share their thoughts on the diagnosis or if they have any other questions. 
10. Lastly, thank the patient for their time and wish them a quick recovery and a good day ahead.  

Keep in mind that you need to act like an actual clinical psychiatrist who knows how to ease the patient into sharing enough info for the diagnosis by keeping the conversation flowing with one question at a time instead of overwhelming the patient with a lot of information in one output.
"""

        max_tokens_suggestions = 1500  # Increase the max_tokens for suggestions

        # Generate response for patient's suggestions
        response_suggestions = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use GPT-3.5 Turbo engine
            messages=[{"role": "system", "content": prompt_suggestions}],
            max_tokens=max_tokens_suggestions
        )
        bot_response_suggestions = response_suggestions['choices'][0]['message']['content'].strip()

        return bot_response_suggestions  # Return only suggestions

    except Exception as e:
        print(f"An error occurred while generating the response: {e}")
        return "Error generating response"


def chat_interaction(session):
    if session:
        print(f"As a {session.specialty} specialist, I'm here to assist you.")
        
        while True:
            user_input = get_user_input()
            if user_input.lower() == "exit":
                break
            store_chat_message(session, {'timestamp': datetime.datetime.now(), 'content': user_input})
            response = generate_medical_response(session.chat_history, session.specialty)
            print("AI Response: ", response)

    else:
        print("Session could not be started.")


session = start_session()
chat_interaction(session)
