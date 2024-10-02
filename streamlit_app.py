import streamlit as st
import time
import openai
import os
import warnings

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# This will print the warning message with more details
warnings.simplefilter("always")

class Quiz:
    def __init__(self, topic):
        self.topic = topic
        self.questions_and_answers, self.raw_response = self.generate_questions()
        self.score = 0
        self.current_question = 0

    def generate_questions(self, num_questions=10):
        prompt = f"Generate {num_questions} yes/no questions about {self.topic}. Format each question on a new line, prefixed with 'Q: '. After each question, on a new line, provide the correct answer prefixed with 'A: ' (yes or no)."
        
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You generate quick questions about a topic. Answers to the questions should be only 'yes' or 'no' disregarding the language in which the user provided the topic"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.7,
        )

        raw_response = response.choices[0].message.content.strip()
        content = raw_response.split('\n')
        questions_and_answers = []
        for i in range(0, len(content), 3):
            if i+1 < len(content):
                question = content[i][3:]  # Remove 'Q: ' prefix
                answer = content[i+1][3:].strip().lower() == 'yes'  # Convert to boolean
                questions_and_answers.append((question, answer))
                
        return questions_and_answers, raw_response

    def check_answer(self, user_answer):
        correct_answer = self.questions_and_answers[self.current_question][1]
        return user_answer == correct_answer, correct_answer

    def next_question(self):
        self.current_question += 1

    def is_finished(self):
        return self.current_question >= len(self.questions_and_answers)

    def get_current_question(self):
        return self.questions_and_answers[self.current_question][0]

def main():
    st.title("Yes/No Quiz App")

    if st.button("Restart Quiz"):
        st.session_state.quiz = None
        st.session_state.timer = None
        st.rerun()
    
    # Sidebar for debugging
    st.sidebar.title("Debug Information")
    if 'quiz' in st.session_state and st.session_state.quiz is not None:
        st.sidebar.text_area("Raw LLM Response", st.session_state.quiz.raw_response, height=300)
        st.sidebar.write("Current Score:", st.session_state.quiz.score)
        st.sidebar.text_area("Content of questions_and_answers", st.session_state.quiz.questions_and_answers, height=300)

    if 'quiz' not in st.session_state:
        st.session_state.quiz = None
        st.session_state.timer = None

    if st.session_state.quiz is None:
        topic = st.text_area("Enter a topic for your quiz:", height=1, max_chars=35)
        if topic != "" and st.session_state.quiz is None:
            with st.spinner("Generating questions..."):
                st.session_state.quiz = Quiz(topic)
            st.session_state.timer = time.time()
            st.rerun()
        
        if st.button("Start Quiz") and topic != "":
            with st.spinner("Generating questions..."):
                st.session_state.quiz = Quiz(topic)
            st.session_state.timer = time.time()
            st.rerun()

    elif not st.session_state.quiz.is_finished():
        st.metric("Current Score", st.session_state.quiz.score)
        st.progress(st.session_state.quiz.score / len(st.session_state.quiz.questions_and_answers))
        
        question = st.session_state.quiz.get_current_question()
        st.write(f"Question {st.session_state.quiz.current_question + 1}: {question}")

        col1, col2 = st.columns(2)
        with col1:
            yes_button = st.button("Yes")
        with col2:
            no_button = st.button("No")

        time_left = max(0, 7 - (time.time() - st.session_state.timer))
        # Will show time left to answer the question.
        #st.write(f"Time left: {time_left:.1f} seconds")

        if yes_button or no_button or time_left == 0:
            user_answer = True if yes_button else (False if no_button else None)
            if user_answer is not None:
                is_correct, correct_answer = st.session_state.quiz.check_answer(user_answer)
                st.session_state.quiz.score += 1 if is_correct else 0
                st.write("Correct!" if is_correct else f"Incorrect. The correct answer was {'Yes' if correct_answer else 'No'}.")
            else:
                st.write("Time's up!")
                _, correct_answer = st.session_state.quiz.check_answer(None)
                st.write(f"The correct answer was {'Yes' if correct_answer else 'No'}.")

            st.session_state.quiz.next_question()
            st.session_state.timer = time.time()
            time.sleep(1.2)  # Give user time to see the result
            st.rerun()

    else:
        st.write(f"Quiz finished! Your score is {st.session_state.quiz.score} out of {len(st.session_state.quiz.questions_and_answers)}.")
        if st.button("Play Again"):
            st.session_state.quiz = None
            st.rerun()

if __name__ == "__main__":
    main()