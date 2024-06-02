import openai
import datetime
import os
import random

# Set up OpenAI API key
openai.api_key = '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'


class UserSession:
    def __init__(self, user_identifier, specialty):
        self.user_identifier = user_identifier
        self.specialty = specialty
        self.chat_history_file = f"{self.specialty}_{self.user_identifier}_chat.txt"
        self.chat_history = []

    def save_chat_message(self, message):
        with open(self.chat_history_file, 'a') as file:
            file.write(f"{datetime.datetime.now()} - {self.user_identifier}: {message}\n")

    def load_chat_history(self):
        if os.path.exists(self.chat_history_file):
            with open(self.chat_history_file, 'r') as file:
                self.chat_history = file.readlines()

    def clear_chat_history(self):
        if os.path.exists(self.chat_history_file):
            os.remove(self.chat_history_file)


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
        user_identifier = input("Enter a user identifier (e.g., A-user): ")
        session = UserSession(user_identifier, specialty)
        return session
    else:
        print("Invalid specialty choice.")
        return None

def get_user_input(prompt):
    return input(prompt + "\n")

def store_chat_message(session, message):
    session.save_chat_message(message)

def ask_patient_question(question):
    user_input = get_user_input(question)
    return user_input

def generate_medical_response(specialty, continuity_prompt):
    prompt_suggestions = f"""Act as an expert clinical psychiatrist to talk to patients with mental health issues in order to accurately diagnose their problems by performing the following steps one by one: 
1.	Greet the patient and introduce yourself as a chatbot trained to help people through their mental health issues 
2.	Make it clear that the information shared here will remain confidential 
3.	Ask for the patient’s introduction 
4.	Get to know the patient by initiating small talk with simple questions like: 
    •	How is your day going? 
    •	How have you been? 
    •	How are you feeling? 
    •	Is there anything bothering you? Would you like to share how you are coping with it? 
5.	Keep asking questions to dive deeper into your patient’s mental state until the patient has given you enough information for an accurate diagnosis 
6.	Once you have a diagnosis, probe the patient with questions to confirm if their symptoms match the mental health issue you have identified. Then, use academic literature and the most credible and updated sources of information in the field of clinical psychiatry to identify and confirm the diagnosis. 
7.	As kindly as possible, explain the mental health issue to the patient and answer all the questions they may have regarding their diagnosis before recommending sources like credible textbooks or papers for further reading 
8.	Lastly, conduct thorough research on the identified issue to create a comprehensive step-by-step plan for the patient’s treatment, which must include usually prescribed medication and mental and physical exercises to treat the identified issue along with reasoning and evidence from credible sources to support the prescribed steps for treatment 
9.	Then, ask the patient if they would like to share their thoughts on the diagnosis or if they have any other questions. 
10.	Lastly, thank the patient for their time and wish them a quick recovery and a good day ahead.  

Keep in mind that you need to act like an actual clinical psychiatrist who knows how to ease the patient into sharing enough info for the diagnosis by keeping the conversation flowing with one question at a time instead of overwhelming the patient with a lot of information in one output.


    {continuity_prompt}"""

    max_tokens_suggestions = 1500
    try:
        response_suggestions = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt_suggestions}],
            max_tokens=max_tokens_suggestions
        )
        bot_response_suggestions = response_suggestions['choices'][0]['message']['content'].strip()

        return bot_response_suggestions

    except Exception as e:
        print(f"An error occurred while generating the response: {e}")
        return "Error generating response"

def chat_interaction(session):
    if session:
        print(f"As a {session.specialty} specialist, I'm here to assist you.")

        session.load_chat_history()
        for message in session.chat_history:
            print(message.strip())

        clear_chat_option = input("Do you want to clear the previous chat and start a new session? (yes/no): ")
        if clear_chat_option.lower() == 'yes':
            session.clear_chat_history()
            print("Starting a new session.")

        questions = [
            "Can you share with me what you've been experiencing lately?",
            "Thank you for sharing that. Can you tell me more about what specifically triggers your mental health concern?",
            "How long have you been experiencing these symptoms?",
            "Have you noticed any patterns or changes in your daily routine that might be contributing to these feelings?"
        ]
        continuity_prompt = "Would you like to share more about your experiences or ask any specific questions?"

        # Asking the four hard-coded questions in a loop
        for question in questions:
            user_input = ask_patient_question(question)
            store_chat_message(session, f"User: {user_input}")

        # Generating medical response based on inputs
        response_suggestions = generate_medical_response(session.specialty, continuity_prompt)
        print("Bot: ", response_suggestions)

        # Looping for continuing or dumping the chat
        while True:
            options = ["1. Continue the conversation", "2. Dump the old chat and start a new session"]
            print("\n".join(options))
            choice = input("Enter the number corresponding to your choice: ")
            if choice == "1":
                user_input = ask_patient_question(continuity_prompt)
                store_chat_message(session, f"User: {user_input}")
                response_suggestions = generate_medical_response(session.specialty, continuity_prompt)
                print("Bot: ", response_suggestions)
            elif choice == "2":
                session.clear_chat_history()
                print("Starting a new session.")

                # Asking the four hard-coded questions in a loop for the new session
                for question in questions:
                    user_input = ask_patient_question(question)
                    store_chat_message(session, f"User: {user_input}")

                # Generating medical response based on inputs for the new session
                response_suggestions = generate_medical_response(session.specialty, continuity_prompt)
                print("Bot: ", response_suggestions)
    else:
        print("Session could not be started.")


session = start_session()
chat_interaction(session)