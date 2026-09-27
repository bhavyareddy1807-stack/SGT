from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "engineering_grades.db"

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Table 1: Student Profile Information
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            usn TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            class_sec TEXT NOT NULL,
            roll_no TEXT NOT NULL,
            attendance REAL NOT NULL,
            gpa REAL NOT NULL
        )
    ''')

    # Table 2: Engineering Subjects linked to Student
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subject_grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject_name TEXT NOT NULL,
            marks REAL NOT NULL,
            credits INTEGER NOT NULL,
            letter_grade TEXT NOT NULL,
            grade_points INTEGER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

# Helper function for engineering grade scale (10-point scale)
def calculate_grade_details(marks):
    if marks >= 90: return "O", 10        # Outstanding
    elif marks >= 80: return "A+", 9     # Excellent
    elif marks >= 70: return "A", 8      # Very Good
    elif marks >= 60: return "B+", 7     # Good
    elif marks >= 50: return "B", 6      # Above Average
    elif marks >= 40: return "C", 5      # Pass
    else: return "F", 0                  # Fail

# --- BACKEND API ROUTES ---

@app.route("/api/students", methods=["GET"])
def get_students():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, usn, email, class_sec, roll_no, attendance, gpa FROM students")
    students_raw = cursor.fetchall()
    
    students = []
    for s in students_raw:
        student_id = s[0]
        cursor.execute("SELECT subject_name, marks, credits, letter_grade FROM subject_grades WHERE student_id = ?", (student_id,))
        subjects = [{"name": sub[0], "marks": sub[1], "credits": sub[2], "grade": sub[3]} for sub in cursor.fetchall()]
        
        students.append({
            "id": s[0], "name": s[1], "usn": s[2], "email": s[3],
            "class_sec": s[4], "roll_no": s[5], "attendance": s[6], "gpa": s[7],
            "subjects": subjects
        })
        
    conn.close()
    return jsonify(students)

@app.route("/api/students", methods=["POST"])
def add_student():
    data = request.json
    
    name = data.get("name")
    usn = data.get("usn")
    email = data.get("email")
    class_sec = data.get("class_sec")
    roll_no = data.get("roll_no")
    attendance = float(data.get("attendance"))
    subjects_data = data.get("subjects", [])

    total_credit_points = 0
    total_credits = 0
    processed_subjects = []

    for sub in subjects_data:
        sub_name = sub.get("name")
        marks = float(sub.get("marks"))
        credits = int(sub.get("credits"))
        letter_grade, grade_points = calculate_grade_details(marks)
        
        total_credit_points += (grade_points * credits)
        total_credits += credits
        processed_subjects.append((sub_name, marks, credits, letter_grade, grade_points))

    gpa = round(total_credit_points / total_credits, 2) if total_credits > 0 else 0.0

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO students (name, usn, email, class_sec, roll_no, attendance, gpa) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, usn, email, class_sec, roll_no, attendance, gpa)
        )
        student_id = cursor.lastrowid

        for sub in processed_subjects:
            cursor.execute(
                "INSERT INTO subject_grades (student_id, subject_name, marks, credits, letter_grade, grade_points) VALUES (?, ?, ?, ?, ?, ?)",
                (student_id, sub[0], sub[1], sub[2], sub[3], sub[4])
            )

        conn.commit()
        return jsonify({"message": "Engineering Record Created!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "USN already exists!"}), 400
    finally:
        conn.close()

@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    cursor.execute("DELETE FROM subject_grades WHERE student_id = ?", (student_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student Deleted"})

# --- PAGE NAVIGATION ROUTES ---

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)