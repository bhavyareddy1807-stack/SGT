document.addEventListener("DOMContentLoaded", () => {
    const studentForm = document.getElementById("studentForm");
    const generateBtn = document.getElementById("generateBtn");
    const container = document.getElementById("subjectsContainer");

    // Dynamic Subject Field Generator
    if (generateBtn) {
        generateBtn.addEventListener("click", () => {
            const count = parseInt(document.getElementById("numSubjects").value) || 1;
            container.innerHTML = "";
            for (let i = 1; i <= count; i++) {
                const div = document.createElement("div");
                div.className = "subject-row";
                div.innerHTML = `
                    <input type="text" class="sub-name" placeholder="Subject Name #${i}" required>
                    <input type="number" class="sub-marks" placeholder="Marks (0-100)" min="0" max="100" step="0.1" required>
                    <input type="number" class="sub-credits" placeholder="Credits (1-6)" min="1" max="6" required>
                `;
                container.appendChild(div);
            }
        });
    }

    // Submit Record and redirect to Dashboard Page
    if (studentForm) {
        studentForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const subjects = [];
            document.querySelectorAll(".subject-row").forEach(row => {
                subjects.push({
                    name: row.querySelector(".sub-name").value,
                    marks: row.querySelector(".sub-marks").value,
                    credits: row.querySelector(".sub-credits").value
                });
            });

            if (subjects.length === 0) {
                alert("Please click 'Configure' to set up subjects first.");
                return;
            }

            const payload = {
                name: document.getElementById("name").value,
                usn: document.getElementById("usn").value,
                email: document.getElementById("email").value,
                class_sec: document.getElementById("class_sec").value,
                roll_no: document.getElementById("roll_no").value,
                attendance: document.getElementById("attendance").value,
                subjects: subjects
            };

            const res = await fetch("/api/students", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (res.ok) {
                window.location.href = "/dashboard"; // Navigate automatically to next page
            } else {
                const err = await res.json();
                alert(err.error || "Submission failed!");
            }
        });
    }

    // Auto-fetch if on Dashboard Page
    if (document.getElementById("recordsList")) {
        fetchStudents();
    }
});

let allStudents = [];

async function fetchStudents() {
    const res = await fetch("/api/students");
    allStudents = await res.json();
    renderDashboard(allStudents);
}

function renderDashboard(students) {
    const list = document.getElementById("recordsList");
    if (!list) return;
    list.innerHTML = "";

    if (students.length === 0) {
        list.innerHTML = `<p style="text-align:center; padding: 40px; color:#64748b;">No matching student records found.</p>`;
        return;
    }

    students.forEach(s => {
        const card = document.createElement("div");
        card.className = "student-excel-card";

        const subjectRows = s.subjects.map(sub => `
            <tr>
                <td>${sub.name}</td>
                <td>${sub.marks}</td>
                <td>${sub.credits}</td>
                <td><strong>${sub.grade}</strong></td>
            </tr>
        `).join('');

        card.innerHTML = `
            <div class="info-summary-bar">
                <!-- Line 1: Identity & GPA -->
                <div class="info-line">
                    <span>Name: <strong>${s.name}</strong></span>
                    <span>USN: <strong>${s.usn}</strong></span>
                    <span class="gpa-badge">GPA: ${s.gpa.toFixed(2)}</span>
                </div>
                <!-- Line 2: Academic Metadata -->
                <div class="info-line">
                    <span>Class/Sec: <strong>${s.class_sec}</strong></span>
                    <span>Roll No: <strong>${s.roll_no}</strong></span>
                    <span>Attendance: <strong>${s.attendance}%</strong></span>
                </div>
                <!-- Line 3: Contact & Sub Count -->
                <div class="info-line">
                    <span>Email: <strong>${s.email}</strong></span>
                    <span>Subjects Enrolled: <strong>${s.subjects.length}</strong></span>
                </div>
            </div>

            <!-- Excel Sheet Columns -->
            <table class="excel-table">
                <thead>
                    <tr>
                        <th>Subject Name</th>
                        <th>Marks Obtained (100)</th>
                        <th>Credits Allocated</th>
                        <th>Letter Grade</th>
                    </tr>
                </thead>
                <tbody>
                    ${subjectRows}
                </tbody>
            </table>

            <div class="action-bar">
                <button class="delete-btn" onclick="deleteStudent(${s.id})">Delete Record</button>
            </div>
        `;

        list.appendChild(card);
    });
}

// Live Search Filter Function
function filterRecords() {
    const query = document.getElementById("searchInput").value.toLowerCase();
    const filtered = allStudents.filter(s =>
        s.name.toLowerCase().includes(query) ||
        s.usn.toLowerCase().includes(query) ||
        s.roll_no.toLowerCase().includes(query) ||
        s.class_sec.toLowerCase().includes(query)
    );
    renderDashboard(filtered);
}

async function deleteStudent(id) {
    if (confirm("Delete this student record permanently?")) {
        await fetch(`/api/students/${id}`, { method: "DELETE" });
        fetchStudents();
    }
}