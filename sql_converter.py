import subprocess
import streamlit as st

def generate_sql(schema: str, question: str) -> str:
    # Enhanced prompt for better SQL generation
    prompt = f"""
You are an intelligent AI trained to convert natural language questions into SQL queries using the given database schema. 

### Instructions:
- Use only the tables and columns provided in the schema.
- Do not assume any extra columns or tables.
- Write clean and valid SQL.
- Use table joins when needed.
- Prefer standard SQL syntax.
- Do NOT include any explanation or extra text. Only output the SQL query.

### Schema:
{schema}

### Question:
{question}

### SQL:
"""

    try:
        result = subprocess.run(
            ['ollama', 'run', 'mistral'],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=300  # Increased timeout
        )

        output = result.stdout.decode().strip()
        return output

    except Exception as e:
        return f"❌ Error: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="Text-to-SQL Generator", page_icon="🧠")

st.title("🧠 Text-to-SQL Generator (Offline using Ollama + Mistral)")

with st.form("sql_form"):
    schema = st.text_area("📄 Enter Database Schema (one table per line)", height=200, placeholder="customers(id, name)\norders(id, customer_id, order_date)")
    question = st.text_input("❓ Enter Your Natural Language Question", placeholder="List the names of customers who placed an order in March.")

    submitted = st.form_submit_button("🧪 Generate SQL")

if submitted:
    if not schema.strip() or not question.strip():
        st.warning("⚠️ Please enter both schema and question.")
    else:
        with st.spinner("Running Mistral..."):
            sql = generate_sql(schema, question)
        st.code(sql, language="sql")



