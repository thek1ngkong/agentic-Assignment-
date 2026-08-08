import re
import requests
from flask import Flask, render_template, request, jsonify
from database import init_db, get_schema, execute_query

app = Flask(__name__)

# Initialize database and seed sample data on app start
init_db()

OLLAMA_API_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3"

def extract_clean_sql(llm_output: str) -> str:
    """
    Strips markdown code blocks, backticks, and extra text from the LLM output
    to extract the raw SQL statement.
    """
    text = llm_output.strip()
    
    # Remove markdown code blocks if present
    sql_match = re.search(r'```(?:sql)?\s*(.*?)\s*```', text, re.DOTALL | re.IGNORECASE)
    if sql_match:
        text = sql_match.group(1).strip()
    
    # Remove single line backtick wrappers or leftover backticks
    text = text.replace("`", "").strip()
    
    # If LLM attached commentary after a semicolon, take only the query up to the semicolon
    if ";" in text:
        text = text.split(";")[0].strip() + ";"
    elif not text.endswith(";"):
        text = text + ";"
        
    return text

def fallback_demo_sql(question: str) -> str:
    """
    Fallback SQL generator when Ollama server is offline or times out.
    """
    q = question.lower()
    numbers = re.findall(r'\d+', q)
    num = numbers[0] if numbers else "80"
    
    if "computer science" in q or "cs" in q:
        return "SELECT * FROM students WHERE department = 'Computer Science';"
    elif "electronics" in q:
        if "order" in q or "descending" in q or "sort" in q:
            return "SELECT name, marks FROM students WHERE department = 'Electronics' ORDER BY marks DESC;"
        return "SELECT * FROM students WHERE department = 'Electronics';"
    elif "mechanical" in q:
        return "SELECT * FROM students WHERE department = 'Mechanical Engineering';"
    elif "civil" in q:
        return "SELECT * FROM students WHERE department = 'Civil Engineering';"
    elif "highest" in q or "maximum" in q or "max" in q or "top" in q:
        return "SELECT name, department, MAX(marks) AS marks FROM students;"
    elif "count" in q or "how many" in q:
        if "department" in q or "each" in q:
            return "SELECT department, COUNT(*) AS total_students FROM students GROUP BY department;"
        return "SELECT COUNT(*) AS total_students FROM students;"
    elif "more than" in q or "greater than" in q or "above" in q or ">" in q:
        return f"SELECT * FROM students WHERE marks > {num};"
    elif "less than" in q or "below" in q or "<" in q:
        return f"SELECT * FROM students WHERE marks < {num};"
    elif "average" in q or "avg" in q:
        return "SELECT AVG(marks) AS average_marks FROM students;"
    else:
        return "SELECT * FROM students;"

@app.route("/")
def index():
    schema = get_schema()
    return render_template("index.html", schema=schema, default_model=DEFAULT_MODEL)

@app.route("/api/schema", methods=["GET"])
def get_db_schema():
    return jsonify({"schema": get_schema()})

@app.route("/ask", methods=["POST"])
def ask_sql():
    data = request.get_json() or {}
    user_question = data.get("question", "").strip()
    model = data.get("model", DEFAULT_MODEL).strip() or DEFAULT_MODEL

    if not user_question:
        return jsonify({"success": False, "error": "Please provide a valid question."}), 400

    schema = get_schema()

    prompt = f"""You are a SQL expert assistant. Convert the user's natural language question into a single valid SQLite SELECT query based ONLY on the provided schema.

Database Schema:
{schema}

Instructions:
1. Return ONLY the raw SQL query.
2. Do NOT write explanations, introduction, markdown headers, or markdown ticks like ```sql.
3. Use only table 'students' and columns: id, name, department, marks.
4. Make the query case-insensitive for text matching when appropriate.

Question: {user_question}
SQL Query:"""

    try:
        # Increased timeout to 120 seconds for LLM model loading on first run
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1
                }
            },
            timeout=120
        )

        if response.status_code == 200:
            llm_response = response.json().get("response", "")
            if llm_response:
                generated_sql = extract_clean_sql(llm_response)
                columns, results = execute_query(generated_sql)
                return jsonify({
                    "success": True,
                    "sql": generated_sql,
                    "columns": columns,
                    "results": results,
                    "source": "Ollama LLM (Llama 3)"
                })

        return jsonify({
            "success": False,
            "error": f"Ollama returned status {response.status_code}: {response.text}"
        }), 500

    except requests.exceptions.Timeout:
        # If Ollama is taking unusually long to load model
        generated_sql = fallback_demo_sql(user_question)
        columns, results = execute_query(generated_sql)
        return jsonify({
            "success": True,
            "sql": generated_sql,
            "columns": columns,
            "results": results,
            "source": "Demo Fallback (LLM Timeout)",
            "warning": "Ollama LLM took longer than expected to load model. Displaying fallback query results."
        })
    except requests.exceptions.ConnectionError:
        generated_sql = fallback_demo_sql(user_question)
        columns, results = execute_query(generated_sql)
        return jsonify({
            "success": True,
            "sql": generated_sql,
            "columns": columns,
            "results": results,
            "source": "Demo Fallback (Ollama Offline)",
            "warning": "Ollama local server is not running on port 11434. Ensure 'ollama serve' is running."
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "sql": generated_sql if 'generated_sql' in locals() else None
        }), 400

if __name__ == "__main__":
    print("Starting Text-to-SQL Assistant Lab server...")
    print("Open http://127.0.0.1:5000 in your browser.")
    app.run(debug=True, host="127.0.0.1", port=5000)
