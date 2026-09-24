# pip install pandas openpyxl ollama tabulate

import pandas as pd
import sqlite3
import re
import ollama

# Working
# Query- What is average Salary of employee?
# Excel --> Sqlite -->Que-->LLM--> SQL Query --> Result -->LLM--> Answer
# another approach for file access
#test_data = r"C:\Users\HP\Downloads\Pro\Genai\basics\test.xlsx"

EXCEL_FILE = "test.xlsx"
#MODEL_NAME = "llama3.2:1b"
MODEL_NAME = "llama3.2:latest"
# excel_data = pd.read_excel(EXCEL_FILE, sheet_name=None)
# print('####',type(excel_data))

def clean_table_name(name):
    name = re.sub(r"\W+", "_", name.strip())
    if not name:
        name = "Sheet"
    return name


def load_excel_to_sqlite(excel_file):
    excel_data = pd.read_excel(excel_file, sheet_name=None)
    print('####',type(excel_data))
    conn = sqlite3.connect(":memory:")

    table_info = {}

    for sheet_name, df in excel_data.items():
        table_name = clean_table_name(sheet_name)

        df.columns = [
            re.sub(r"\W+", "_", str(col).strip()) for col in df.columns
        ]

        df.to_sql(table_name, conn, index=False, if_exists="replace")

        table_info[table_name] = {
            "original_sheet": sheet_name,
            "columns": list(df.columns),
            "sample_rows": df.head(3).to_dict(orient="records")
        }

    return conn, table_info


def ask_ollama_for_sql(question, table_info):
    schema_text = ""

    for table_name, info in table_info.items():
        schema_text += f"\nTable: {table_name}\n"
        schema_text += f"Columns: {', '.join(info['columns'])}\n"
        schema_text += f"Sample rows: {info['sample_rows']}\n"

    prompt = f"""
You are an expert data analyst.

The user has an Excel file loaded into SQLite tables.

Schema:
{schema_text}

User question:
{question}

Task:
Write only one valid SQLite SQL query to answer the question.

Rules:
- Return only SQL query.
- Do not explain.
- Do not use markdown.
- Use only the table and column names provided.
- If question asks count, sum, average, max, min, group by, use SQL aggregation.
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    sql = response["message"]["content"].strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql


def execute_sql(conn, sql):
    try:
        result = pd.read_sql_query(sql, conn)
        return result, None
    except Exception as e:
        return None, str(e)


def explain_result(question, sql, result_df):
    result_text = result_df.to_markdown(index=False)

    prompt = f"""
User asked:
{question}

SQL used:
{sql}

SQL result:
{result_text}

Give a clear and simple answer based only on the SQL result.
Do not add extra assumptions.
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"].strip()


def main():
    # Load Excel file into SQLite
    conn, table_info = load_excel_to_sqlite(EXCEL_FILE)

    print("Excel file loaded successfully.")
    print("Available sheets/tables:")
    for table in table_info:
        print("-", table)

    while True:
        question = input("\nAsk question about Excel file or type 'exit': ")

        if question.lower() in ["exit", "quit"]:
            break
        
        # Ask LLM to generate SQL query
        sql = ask_ollama_for_sql(question, table_info)
        print("\nGenerated SQL:")
        print(sql)

        # Execute SQL query
        result_df, error = execute_sql(conn, sql)

        if error:
            print("\nError while running SQL:")
            print(error)
            continue

        print("\nResult:")
        print(result_df)
        # Explain the result using LLM
        final_answer = explain_result(question, sql, result_df)

        print("\nAnswer:")
        print(final_answer)


if __name__ == "__main__":
    main()


