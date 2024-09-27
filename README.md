**QuizApp **
QuizApp is a dynamic quiz application built using Django. It allows users to take quizzes in various categories, tracks their scores, and provides detailed results. The app supports user registration, login, logout, and quiz history tracking.

**Features **
**User Authentication**: Register, login, and logout functionality with CSRF protection.

**Quiz System:** Quizzes are categorized for better organization. Questions are dynamically generated, and all questions are presented on a single page.

**Scoring & Results**: Users can submit their answers and receive their scores immediately. Detailed feedback on the submitted answers, showing the correct answers and user responses.

**Quiz History:** Users can view their quiz history, tracking their past performance.

**Installation Prerequisites **
Before you begin, ensure you have the following installed:

Python 3.10+ 
Django 4.1.1 
A virtual environment tool (e.g., virtualenv or venv)

**Steps**
Clone the repository: https://github.com/Dominicksam/ALX-Portfolio-Project--Quiz-App
cd QuizApp Create and activate a virtual environment:
run python -m venv env source env/bin/activate # On Windows 
use env\Scripts\activate Install the required packages: 
pip install -r requirements.txt 
Run migrations to set up the database: 
python manage.py migrate Create a superuser to access the Django admin: 
python manage.py createsuperuser Run the development server:
python manage.py runserver Access the application:

Open your browser and go to http://127.0.0.1:8000/.

Usage Register an Account: Users can register by providing a username, email, and password.

Login: Once registered, users can log in using their credentials.

Taking a Quiz:

After login, users can select quizzes based on different categories. Quizzes are timed, and all questions are displayed on a single page. Users can answer multiple-choice questions and submit their answers. View Results:

After submitting a quiz, users receive their scores immediately, with detailed feedback. The quiz history is available through a dropdown button on the result page. App Structure Authentication: Manages user registration, login, and logout. Quiz: Manages quiz categories, questions, and quiz-taking logic. Results: Handles the display of scores and feedback after quiz completion. Quiz History: Displays the user's past quizzes and scores.

SCREENSHOT
![Screenshot (221)](https://github.com/user-attachments/assets/e585f76c-d532-4f00-a642-1c7a10e50be8)
![Screenshot (219)](https://github.com/user-attachments/assets/76a708f1-8275-4cad-a78c-58ae9a2a8138)






License This project is licensed under the MIT License. See the LICENSE file for more details.
