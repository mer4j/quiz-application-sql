# Prescribed Criteria:
- The application provides a user interface for students to answer multiple choice questions  presented to them.
- After answering questions, the application gives feedback to students based on their performance, indicating whether their answers were correct or incorrect.
- The application allows editing of the quiz database, enabling instructors to modify existing quizzes or create new ones for future use.
- Questions for quizzes are retrieved from the database, ensuring variability in quiz content and allowing instructors to generate different quizzes.
- The application generates an external backup file to store important data, ensuring that quiz information and student responses are securely saved
  
# Self-Defined Criteria:
- The application stores quiz questions, student responses, and results in an SQLite database format, ensuring efficient data management and retrieval.
- An algorithm is integrated into the application to analyse student responses for specific keywords or patterns, allowing for more nuanced assessment.
- Upon completion of quizzes, the application adds the students' results to the database, enabling instructors to track progress over time.
- Questions are initially stored in the database, facilitating quick and efficient retrieval by the application when generating quizzes or analysing results.

