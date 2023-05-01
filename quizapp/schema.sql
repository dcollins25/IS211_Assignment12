CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL
);

CREATE TABLE quizzes (
    id INTEGER PRIMARY KEY,
    subject TEXT NOT NULL,
    num_questions INTEGER NOT NULL,
    date_given TEXT NOT NULL
);

CREATE TABLE quiz_results (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    quiz_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
);
