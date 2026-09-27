# Engineering Student Grade Tracker 🎓

A full-stack web application designed for engineering students and academic administrators to record, manage, and track student academic performance using credit-weighted Grade Point Average (GPA) calculations.

Built through the complete **Software Development Life Cycle (SDLC)** using **Flask (Python)**, **SQLite3**, **HTML5/CSS3**, and **Vanilla JavaScript**.

---

## 📌 Features

- **Structured Student Profiling:** Captures complete academic metadata across 3 clean lines (Name, USN, Roll No, Class & Section, Attendance, and Email).
- **Credit-Based GPA Calculation:** Automatically calculates total credit points, grade letters ($O, A+, A, B+, B, C, F$), and Overall GPA (10-point scale) based on subject credits and scores.
- **Dedicated Dashboard & Live Search:** Separate records page featuring real-time client-side search filtering by Name, USN, Roll No, or Class/Section.
- **Excel-Style Data Display:** Displays subjects, marks, credits, and grades in a clean tabular grid format.
- **Relational Database Storage:** Uses SQLite3 with foreign key cascading to maintain linked student profiles and subject grades permanently.

---

## 📁 Directory Structure

```text
Student_Grade_Tracker/
│
├── app.py                  # Flask Backend Server & SQLite API Endpoints
├── engineering_grades.db   # SQLite Relational Database (Generated automatically)
├── static/
│   ├── style.css           # UI Styling (3-line layout & Excel-style tables)
│   └── script.js           # Fetch API Calls & Dynamic Form Controls
└── templates/
    ├── index.html          # Page 1: Student & Subject Registration Form
    └── dashboard.html      # Page 2: Student Records Dashboard & Live Search