# Text-to-SQL Assistant Lab 🎓

A lightweight, beginner-friendly **Text-to-SQL Lab Application** built using **Python**, **Flask**, **SQLite**, and **Ollama (Llama 3)**.

Converts natural English questions into valid SQLite queries, runs them against a pre-populated `college.db` database, and displays the generated SQL statement along with the execution result table.

---

## 🌟 Features

- **Natural Language to SQL Translation:** Translates user questions into SQLite `SELECT` statements using local LLMs.
- **Automated Database Setup:** Automatically creates `college.db` and populates the `students` table with 10 sample records if it doesn't exist.
- **100% Free & Local:** Uses local Ollama (Llama 3) with no external API keys or subscription fees required.
- **Glassmorphic UI:** Modern web dashboard featuring dark mode, interactive query chips, one-click copy SQL button, and dynamic results table.
- **Offline Fallback Engine:** Built-in fallback generator ensures the app remains interactive even when the local AI server is offline.

---

## 📁 Project Structure

```text
text_to_sql/
│
├── app.py              # Flask server, prompt construction & Ollama API integration
├── database.py         # SQLite setup, sample data seeding & safe query executor
├── requirements.txt    # Python package dependencies
├── README.md           # Project documentation
├── .gitignore          # Git ignore rules
│
├── templates/
│   └── index.html      # Glassmorphic web UI
│
└── static/
    └── style.css       # Modern dark-theme styles
```

---

## 🗄️ Database Schema (`college.db`)

**Table:** `students`

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER | Primary Key (Auto Increment) |
| `name` | TEXT | Student full name |
| `department` | TEXT | Department (e.g. Computer Science, Electronics, Mechanical) |
| `marks` | INTEGER | Marks scored (0 - 100) |

---

## 🧪 Sample Questions to Test

1. `Show students who scored more than 80`
2. `List all students in the Computer Science department`
3. `What is the highest marks scored by any student?`
4. `Show student name and marks for Electronics department ordered by marks descending`
5. `Count how many students are in each department`

---

## 🚀 Installation & Running

### 1. Install & Run Ollama
Download Ollama from [ollama.com](https://ollama.com/download) and pull the Llama 3 model:
```bash
ollama pull llama3
```

### 2. Setup Project Environment
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/text-to-sql-lab.git
cd text-to-sql-lab

# Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Start the Web App
```bash
python app.py
```

Open **`http://127.0.0.1:5000`** in your browser.
