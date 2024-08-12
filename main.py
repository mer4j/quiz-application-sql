# Author: mer4j  from github

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.uix.checkbox import CheckBox
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
import login
import sqlite3
import datetime

class TeacherLoginScreen(Screen):
    def __init__(self, **kwargs):
        super(TeacherLoginScreen, self).__init__(**kwargs)
        
        layout = GridLayout(cols=1, spacing=10)

        heading = Label(text="Teacher login", size_hint_y=None, height=40, font_size=20, underline=True)
        layout.add_widget(heading)

        back_button = Button(text='Back', size_hint_y=None, height=40)
        back_button.bind(on_press=self.go_to_main_menu)
        layout.add_widget(back_button)
        self.username_input = TextInput(hint_text='Username')
        self.password_input = TextInput(hint_text='Password', password=True)
        self.email_input = TextInput(hint_text='Email')
        self.phone_input = TextInput(hint_text='Phone Number')

        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.email_input)
        layout.add_widget(self.phone_input)

        login_button = Button(text='Login', size_hint_y=None, height=40)
        login_button.bind(on_press=self.login_teacher)
        layout.add_widget(login_button)

        self.error_label = Label(text="", color=(1, 0, 0, 1))
        layout.add_widget(self.error_label)

        self.add_widget(layout)

    def go_to_main_menu(self, instance):
        self.manager.current = 'main_menu'

    def login_teacher(self, instance):
        if not all([self.username_input.text, self.password_input.text, self.email_input.text, self.phone_input.text]):
            self.error_label.text = "Do not leave any empty fields"
            Clock.schedule_once(self.clear_error, 3)
        else:
            self.perform_teacher_login_action()

    def perform_teacher_login_action(self):
        login.teacher_login("".join(str(self.username_input.text).split()), self.password_input.text, self.email_input.text, self.phone_input.text)
        self.manager.current = 'quiz_screen'
        
    def clear_error(self, dt):
        self.error_label.text = ""


class StudentLoginScreen(Screen):
    def __init__(self, **kwargs):
        super(StudentLoginScreen, self).__init__(**kwargs)
        
        layout = GridLayout(cols=1, spacing=10)

        self.quiz_score_label = Label(text='', size_hint_y=None, height=40)
        self.current_score = 0
        self.total_questions_attempted = 0
        self.total_questions = 0
        self.feedback = ""

        heading = Label(text="Student login", size_hint_y=None, height=40, font_size=20, underline=True)
        layout.add_widget(heading)

        back_button = Button(text='Back', size_hint_y=None, height=40)
        back_button.bind(on_press=self.go_to_main_menu)
        layout.add_widget(back_button)

        self.name_input = TextInput(hint_text='Name')
        self.username_input = TextInput(hint_text='Username')
        self.password_input = TextInput(hint_text='Password', password=True)
        self.email_input = TextInput(hint_text='Email')

        layout.add_widget(self.name_input)
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.email_input)

        login_button = Button(text='Login', size_hint_y=None, height=40)
        login_button.bind(on_press=self.login_student)
        layout.add_widget(login_button)

        self.error_label = Label(text="", color=(1, 0, 0, 1))
        layout.add_widget(self.error_label)

        self.add_widget(layout)

    def go_to_main_menu(self, instance):
        self.manager.current = 'main_menu'

    def login_student(self, instance):
        if not all([self.name_input.text, self.username_input.text, self.password_input.text, self.email_input.text]):
            self.error_label.text = "Do not leave any empty fields"
            Clock.schedule_once(self.clear_error, 3)
        else:
            self.perform_student_login_action()

    def perform_student_login_action(self):
        login.student_login(self.name_input.text, "".join(str(self.username_input.text).split()), self.password_input.text, self.email_input.text)
        self.display_quiz_selection()

    def display_quiz_selection(self):
        self.clear_widgets()

        layout = GridLayout(cols=1, spacing=10)

        quiz_heading = Label(text="Select The Quiz:", size_hint_y=None, height=40, font_size=20, underline=True)
        layout.add_widget(quiz_heading)

        quizzes = self.fetch_quizzes()

        for quiz in quizzes:
            quiz_info = BoxLayout(size_hint_y=None, height=40)
            name_label = Label(text=quiz[1], size_hint_x=0.33, halign='center')
            subject_label = Label(text=quiz[2], size_hint_x=0.33, halign='center')
            info_label = Label(text=quiz[3], size_hint_x=0.33, halign='center')
            attempt_button = Button(text="Attempt", size_hint_x=None, width=100)
            attempt_button.bind(on_press=lambda instance, q=quiz: self.attempt_quiz(q))
            quiz_info.add_widget(name_label)
            quiz_info.add_widget(subject_label)
            quiz_info.add_widget(info_label)
            quiz_info.add_widget(attempt_button)
            layout.add_widget(quiz_info)

        self.add_widget(layout)

        feedback = Label(text=self.feedback, size_hint_y=None, height=40, font_size=20)
        layout.add_widget(feedback)
        
    choice_buttons = []

    def attempt_quiz(self, quiz):
        layout = self.children[0]
        layout.clear_widgets()

        questions = self.fetch_questions_for_quiz(quiz[0])

        if questions:
            first_question = questions[0]
            question_label = Label(text=first_question[1], size_hint_y=None, height=40, font_size=18)
            layout.add_widget(question_label)

            self.choice_buttons.clear()
            for i in range(4):
                choice_button = ToggleButton(text=first_question[i+2], group='choices', size_hint_y=None, height=40, font_size=16)
                layout.add_widget(choice_button)
                self.choice_buttons.append(choice_button)

            submit_button = Button(text="Submit Answer", size_hint_y=None, height=40)
            submit_button.bind(on_press=lambda instance: self.submit_answer(quiz[0], first_question[0], instance))
            layout.add_widget(submit_button)

    def fetch_questions_for_quiz(self, quiz_id):
        connection = sqlite3.connect('quiz.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM questions WHERE quizID=?", (quiz_id,))
        questions = cursor.fetchall()

        cursor.close()
        connection.close()

        return questions
    def submit_answer(self, quiz_id, question_id, instance):
        self.total_questions_attempted += 1
        if self.process_answer_submission(quiz_id, question_id):
            self.current_score += 1

        self.load_next_question(quiz_id, question_id)

    def process_answer_submission(self, quiz_id, question_id):
        connection = sqlite3.connect('quiz.db')
        cursor = connection.cursor()

        cursor.execute("SELECT answers FROM questions WHERE questionID=?", (question_id,))
        correct_answer = str(cursor.fetchone()[0])[0]

        selected_answer = ""
        lngth = 0
        
        for button in self.choice_buttons:
            if button.state == 'down':
                selected_answer = str(lngth+1)
                break
            lngth += 1

        if selected_answer == correct_answer:
            return True
        else:
            return False


        


    def display_question(self, quiz_id, question):
        layout = self.children[0]
        layout.clear_widgets()

        question_label = Label(text=question[1], size_hint_y=None, height=40, font_size=18)
        layout.add_widget(question_label)
        self.choice_buttons.clear()
        for i in range(4):
            choice_button = ToggleButton(text=question[i+2], group='choices', size_hint_y=None, height=40, font_size=16)
            layout.add_widget(choice_button)
            self.choice_buttons.append(choice_button) 

        submit_button = Button(text="Submit Answer", size_hint_y=None, height=40)
        submit_button.bind(on_press=lambda instance: self.submit_answer(quiz_id, question[0], instance))
        layout.add_widget(submit_button)
        
    def get_student_id_by_username(self, username):
        try:
            connection = sqlite3.connect('quiz.db')
            cursor = connection.cursor()
            cursor.execute("SELECT studentID FROM student WHERE username = ?", (username,))
            student_id = cursor.fetchone()

            if student_id:
                return student_id[0]
            else:
                return None

        except sqlite3.Error as error:
            print("Error while connecting to SQLite", error)
            return None

        finally:
            if connection:
                connection.close()
                
    def load_next_question(self, quiz_id, current_question_id):
        questions = self.fetch_questions_for_quiz(quiz_id)
        self.total_questions = len(questions)

        current_question_index = None
        for i, question in enumerate(questions):
            if question[0] == current_question_id:
                current_question_index = i
                break

        if current_question_index is not None:
            next_question_index = current_question_index + 1
            if next_question_index < len(questions):
                next_question = questions[next_question_index]
                self.display_question(quiz_id, next_question)
            else:
                if self.current_score == self.total_questions_attempted:
                    feedback = (f"Congratulations! You got perfect marks of {self.current_score}/{self.total_questions_attempted}")
                elif self.current_score > (self.total_questions_attempted // 2):
                    feedback = (f"Well done! You passed with {self.current_score}/{self.total_questions_attempted} marks.")

                elif self.current_score <= (self.total_questions_attempted // 2) and self.current_score != 0:
                    feedback = (f"You failed with low marks of {self.current_score}/{self.total_questions_attempted}, study harder!")
                else:
                    feedback = ("You didn't get a single answer correct, zero.")

                
                self.feedback = feedback

                
                
                self.update_results_table(quiz_id, f"{self.current_score}/{self.total_questions_attempted}", self.get_student_id_by_username(self.username_input.text))

                self.total_questions_attempted = 0
                self.current_score = 0
                self.display_quiz_selection()


    def update_results_table(self, quiz_id, score_string, student_id):
        connection = sqlite3.connect('quiz.db')
        cursor = connection.cursor()

        completion_date = datetime.datetime.now().strftime('%d%m%Y')

        try:
            cursor.execute("INSERT OR REPLACE INTO results (quizID, studentID, student_score, quiz_completion_date) VALUES (?, ?, ?, ?)",
                           (quiz_id, student_id, score_string, completion_date))

            connection.commit()
        except sqlite3.Error as e:
            print("Error updating results table:", e)

        cursor.close()
        connection.close()

            
    def fetch_questions_for_quiz(self, quiz_id):
        connection = sqlite3.connect('quiz.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM questions WHERE quizID=?", (quiz_id,))
        questions = cursor.fetchall()

        cursor.close()
        connection.close()

        return questions

    def fetch_quizzes(self):
        connection = sqlite3.connect('quiz.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM quiz")
        quizzes = cursor.fetchall()

        cursor.close()
        connection.close()

        return quizzes



    def clear_error(self, dt):
        self.error_label.text = ""



class MyApp(App):

    def build(self):
        self.screen_manager = ScreenManager()
        


        main_menu_screen = Screen(name='main_menu')
        main_menu_layout = GridLayout(cols=1, spacing=10)
        
        with main_menu_layout.canvas.before:
            Color(0, 0, 0, 1)
            self.rect = Rectangle(size=(800, 600), pos=main_menu_layout.pos)
        
        heading = Label(text="Are you a student or teacher?", size_hint_y=None, height=40, font_size=20, underline=True)
        main_menu_layout.add_widget(heading)

        spacer = Label(size_hint_y=None, height=200)
        main_menu_layout.add_widget(spacer)

        buttons_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=120)
        student_button = Button(text='Student', size_hint_y=None, height=40)
        teacher_button = Button(text='Teacher', size_hint_y=None, height=40)
        exit_button = Button(text='Exit', size_hint_y=None, height=40)

        buttons_layout.add_widget(student_button)
        buttons_layout.add_widget(teacher_button)
        buttons_layout.add_widget(exit_button)

        main_menu_layout.add_widget(buttons_layout)
        main_menu_screen.add_widget(main_menu_layout)

        self.screen_manager.add_widget(main_menu_screen)
        self.screen_manager.add_widget(TeacherLoginScreen(name='teacher_login'))
        self.screen_manager.add_widget(StudentLoginScreen(name='student_login'))
        self.screen_manager.add_widget(QuizScreen(name='quiz_screen'))

        self.title = 'QuizMaster'

        teacher_button.bind(on_press=self.switch_to_teacher_login)
        student_button.bind(on_press=self.switch_to_student_login)

        return self.screen_manager

    def switch_to_teacher_login(self, instance):
        self.screen_manager.current = 'teacher_login'

    def switch_to_student_login(self, instance):
        self.screen_manager.current = 'student_login'


class QuizScreen(Screen):
    def __init__(self, **kwargs):
        super(QuizScreen, self).__init__(**kwargs)

        self.layout = GridLayout(cols=1, spacing=10)
        self.add_widget(self.layout)

    def display_quizzes(self):
        self.layout.clear_widgets()

        heading = Label(text="Select the following:", size_hint_y=None, height=40, font_size=20, underline=True)
        self.layout.add_widget(heading)

        quizzes = self.fetch_quizzes()

        for quiz in quizzes:
            quiz_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)

            quiz_label = Label(text=quiz[2])  
            quiz_layout.add_widget(quiz_label)

            delete_button = Button(text='Delete', size_hint_x=None, width=100)
            delete_button.bind(on_press=lambda instance, qid=quiz[0]: self.delete_quiz(qid))
            quiz_layout.add_widget(delete_button)

            add_question_button = Button(text='Add Question', size_hint_x=None, width=150)
            add_question_button.bind(on_press=lambda instance, qid=quiz[0]: self.add_question(qid))
            quiz_layout.add_widget(add_question_button)

            self.layout.add_widget(quiz_layout)

        add_quiz_button = Button(text='Add a Quiz', size_hint_y=None, height=40)
        add_quiz_button.bind(on_press=self.add_quiz)
        self.layout.add_widget(add_quiz_button)

        view_results_button = Button(text='View student results', size_hint_y=None, height=40)
        view_results_button.bind(on_press=self.show_student_results)
        self.layout.add_widget(view_results_button)

    def fetch_quizzes(self):
        connection = sqlite3.connect('quiz.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM quiz")
        quizzes = cursor.fetchall()

        cursor.close()
        connection.close()

        return quizzes

    def delete_quiz(self, quiz_id):
        connection = sqlite3.connect('quiz.db')
        cursor = connection.cursor()

        try:
            cursor.execute("DELETE FROM questions WHERE quizID=?", (quiz_id,))

            cursor.execute("DELETE FROM quiz WHERE quizID=?", (quiz_id,))

            cursor.execute("DELETE FROM results WHERE quizID=?", (quiz_id,))


            connection.commit()

            cursor.close()
            connection.close()

            self.display_quizzes()

        except sqlite3.Error as e:
            print("Error deleting quiz:", e)

    def add_question(self, quiz_id):
        self.layout.clear_widgets()

        create_question_heading = Label(text="Create Question", size_hint_y=None, height=40, font_size=20, underline=True)
        self.layout.add_widget(create_question_heading)

        question_input = TextInput(hint_text='Question', size_hint_y=None, height=40)
        self.layout.add_widget(question_input)

        choice_inputs = []
        for i in range(4):
            choice_input = TextInput(hint_text=f'Choice {i+1}', size_hint_y=None, height=40)
            choice_inputs.append(choice_input)
            self.layout.add_widget(choice_input)


        answer_input = TextInput(hint_text='Answer (1 to 4)', size_hint_y=None, height=40)
        self.layout.add_widget(answer_input)


        create_question_button = Button(text='Create', size_hint_y=None, height=40)
        create_question_button.bind(on_press=lambda instance: self.create_question(quiz_id, question_input.text, [choice_input.text for choice_input in choice_inputs], answer_input.text))
        self.layout.add_widget(create_question_button)


        back_button = Button(text='Back', size_hint_y=None, height=40)
        back_button.bind(on_press=lambda instance: self.display_quizzes())

        self.layout.add_widget(back_button)



    def create_question(self, quiz_id, question, choices, answer):
        connection = sqlite3.connect('quiz.db')
        cursor = connection.cursor()

        cursor.execute("INSERT INTO questions (multiple_choice, choice_one, choice_two, choice_three, choice_four, quizID, answers) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (question, choices[0], choices[1], choices[2], choices[3], quiz_id, answer))


        connection.commit()


        cursor.close()
        connection.close()

        self.display_quizzes()
        create_question_heading = Label(text="Question created successfully!", size_hint_y=None, height=40, font_size=20)
        self.layout.add_widget(create_question_heading)

    def add_quiz(self, instance):
        self.layout.clear_widgets()

        quiz_name_label = Label(text="Quiz Name:", size_hint_y=None, height=40)
        self.layout.add_widget(quiz_name_label)
        self.quiz_name_input = TextInput(hint_text='Enter quiz name', size_hint_y=None, height=40)
        self.layout.add_widget(self.quiz_name_input)

        subject_label = Label(text="Subject Name:", size_hint_y=None, height=40)
        self.layout.add_widget(subject_label)
        self.subject_input = TextInput(hint_text='Enter subject name', size_hint_y=None, height=40)
        self.layout.add_widget(self.subject_input)

        details_label = Label(text="Details:", size_hint_y=None, height=40)
        self.layout.add_widget(details_label)
        self.details_input = TextInput(hint_text='Enter quiz details', size_hint_y=None, height=40)
        self.layout.add_widget(self.details_input)

        create_quiz_button = Button(text='Create Quiz', size_hint_y=None, height=40)
        create_quiz_button.bind(on_press=self.create_quiz)
        self.layout.add_widget(create_quiz_button)

        back_button = Button(text='Back', size_hint_y=None, height=40)
        back_button.bind(on_press=lambda instance: self.display_quizzes())

        self.layout.add_widget(back_button)




    def create_quiz(self, instance):
        teacher_username = self.manager.get_screen('teacher_login').username_input.text

        teacher_id = self.get_teacher_id_from_database(teacher_username)

        quiz_name = self.quiz_name_input.text
        subject_name = self.subject_input.text
        quiz_details = self.details_input.text

        if not all([quiz_name, subject_name, quiz_details]):
            error_label = Label(text="Please fill in all fields", size_hint_y=None, height=40, color=(1, 0, 0, 1))
            self.layout.add_widget(error_label)
            Clock.schedule_once(lambda dt: self.layout.remove_widget(error_label), 1) 
            return

        self.add_quiz_to_database(quiz_name, subject_name, quiz_details, teacher_id)

        self.quiz_name_input.text = ''
        self.subject_input.text = ''
        self.details_input.text = ''

        self.display_quizzes()




    def get_teacher_id_from_database(self, username):
        connection = sqlite3.connect('quiz.db')
        cursor = connection.cursor()

        cursor.execute("SELECT teacherID FROM teacher WHERE username=?", (username,))
        teacher_id = cursor.fetchone()[0] 

        cursor.close()
        connection.close()

        return teacher_id

    def add_quiz_to_database(self, quiz_name, subject_name, quiz_details, teacher_id):
        connection = sqlite3.connect('quiz.db')
        cursor = connection.cursor()

        cursor.execute("INSERT INTO quiz (quiz_subject, quiz_name, quiz_details, teacherID) VALUES (?, ?, ?, ?)",
                       (subject_name, quiz_name, quiz_details, teacher_id))

        connection.commit()

        cursor.close()
        connection.close()

        
    def show_student_results(self, instance):
        self.layout.clear_widgets()
        view_results_heading = Label(text="View Student Results", size_hint_y=None, height=40, font_size=20, underline=True)
        self.layout.add_widget(view_results_heading)

        username_label = Label(text="Enter Student Username:", size_hint_y=None, height=40)
        self.layout.add_widget(username_label)

        username_input = TextInput(size_hint_y=None, height=40)
        self.layout.add_widget(username_input)

        search_button = Button(text='Search', size_hint_y=None, height=40)
        search_button.bind(on_press=lambda instance: self.search_student_results(username_input.text))
        self.layout.add_widget(search_button)

        back_button = Button(text='Back', size_hint_y=None, height=40)
        back_button.bind(on_press=lambda instance: self.display_quizzes())
        self.layout.add_widget(back_button)

    def search_student_results(self, username):
        connection = sqlite3.connect('quiz.db')
        cursor = connection.cursor()

        cursor.execute("SELECT studentID, name FROM student WHERE username=?", (username,))
        student_info = cursor.fetchone()
        if student_info:
            student_id, student_name = student_info

            cursor.execute("SELECT quizID, student_score, quiz_completion_date FROM results WHERE studentID=?", (student_id,))
            student_results = cursor.fetchall()

            quiz_names = {}

            for result in student_results:
                quiz_id = result[0]
                cursor.execute("SELECT quiz_name FROM quiz WHERE quizID=?", (quiz_id,))
                quiz_name = cursor.fetchone()[0]
                quiz_names[quiz_id] = quiz_name


            self.layout.clear_widgets()
            self.display_quizzes()
            for result in student_results:
                quiz_id, score, completion_date = result

                completion_date = datetime.datetime.strptime(str(completion_date), "%d%m%Y").strftime("%d-%m-%Y")
                
                quiz_name = quiz_names.get(quiz_id, "Unknown Quiz") 
                result_label = Label(text=f"Quiz: {quiz_name}, Score: {score}, Completion Date: {completion_date}", size_hint_y=None, height=40)
                self.layout.add_widget(result_label)

        else:
            error_label = Label(text="Student not found", size_hint_y=None, height=40, color=(1, 0, 0, 1))
            self.layout.add_widget(error_label)
            Clock.schedule_once(lambda dt: self.layout.remove_widget(error_label), 1)

        cursor.close()
        connection.close()

    def on_enter(self):
        self.display_quizzes()




if __name__ == '__main__':
    MyApp().run()
