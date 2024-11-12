import streamlit as st
from PIL import Image
import time

# Set the title of the app
st.title("System to detect Personality mood based on EEG sygnals")

# Load the images
sad_image = Image.open("sad.png")
happy_image = Image.open("happy.png")

col1, col2 = st.columns(2)
# Create a toggle state to switch images
if 'toggle' not in st.session_state:
    st.session_state.toggle = False
if 'question' not in st.session_state:
    st.session_state.question = "How can I help you?"

if 'question_index' not in st.session_state:
    st.session_state.question_index = None  # Start with no question selected
if 'responses' not in st.session_state:
    st.session_state.responses = []  # Store answers to questions    

clarification_questions = [
    ("Do you feel physically tired?", "Sadness"),
    ("Are you feeling overwhelmed with responsibilities?", "Fear"),
    ("Have you had enough sleep recently?", "Sadness"),
    ("Do you feel a lack of motivation?", "Anger"),
    ("Are you experiencing physical discomfort (e.g., headache)?", "Anger")
]


with col1:

    # Toggle the image every 5 seconds
    st.session_state.toggle = not st.session_state.toggle
    image_to_show = sad_image if st.session_state.toggle else happy_image
    caption = "Sad Image" if st.session_state.toggle else "Happy Image"

    # Display the image
    st.image(image_to_show, caption=caption, use_column_width=True)


with col2:
    if st.session_state.question_index is None:
        # Initial question before starting the clarification process
        st.header("How can I help you?")
        if st.button("Play music"):
            st.write("Playing music to cheer you up!")

            if st.button("Return to Home"):
                st.session_state.question_index = None    
                st.session_state.responses = []         
 
        elif st.button("Clarify my emotional state"):
            st.session_state.question_index = 0   
            st.session_state.responses = []       

    elif st.session_state.question_index < len(clarification_questions):

        current_question, emotion = clarification_questions[st.session_state.question_index]
        st.header(current_question)
  
        if st.button("Yes"):
            st.session_state.responses.append(emotion)   
            st.session_state.question_index += 1  
        elif st.button("No"):
            st.session_state.responses.append(None)   
            st.session_state.question_index += 1  

    else:
        emotion_count = {"Anger": 0, "Fear": 0, "Sadness": 0}
        for response in st.session_state.responses:
            if response:
                emotion_count[response] += 1

        # Determine the dominant emotion
        dominant_emotion = max(emotion_count, key=emotion_count.get)
        st.header(f"You are likely feeling: {dominant_emotion}")
        # st.subheader(f"You are likely feeling: {dominant_emotion}")
 
        if st.button("Return to Home"):
            st.session_state.question_index = None   
            st.session_state.responses = []          
            st.session_state.question = "How can I help you?"   
 
time.sleep(5)
st.experimental_rerun()