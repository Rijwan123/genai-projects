# pip install pandas openpyxl ollama tabulate
# For old .xls files:
# pip install xlrd

import pandas as pd
import sqlite3
import re
import ollama

from pathlib import Path
from urllib.parse import urlparse, unquote


DEFAULT_FILE = "test.xlsx"
#MODEL_NAME = "llama3.2:1b"
MODEL_NAME = "llama3.2:latest"



# ---------------------------------------------------------
# Cleaning functions
# ---------------------------------------------------------

def clean_identifier(name, default_name="Column"):
    """
    Converts table and column names into SQLite-friendly names.
    """

    name = re.sub(r"\W+", "_", str(name).strip())
    name = name.strip("_")

    if not name:
        name = default_name

    # SQLite identifiers should not begin with a number.
    if name[0].isdigit():
        name = f"_{name}"

    return name


def make_unique_names(names):
    """
    Makes cleaned column names unique.

    Example:
        Salary, Salary -> Salary, Salary_2
    """

    unique_names = []
    name_counts = {}

    for name in names:
        clean_name = clean_identifier(name)

        if clean_name not in name_counts:
            name_counts[clean_name] = 1
            unique_names.append(clean_name)
        else:
            name_counts[clean_name] += 1
            unique_names.append(
                f"{clean_name}_{name_counts[clean_name]}"
            )

    return unique_names


# ---------------------------------------------------------
# File path and URL handling
# ---------------------------------------------------------

def is_url(source):
    return source.lower().startswith(("http://", "https://"))


def convert_github_url_to_raw(source):
    """
    Converts a normal GitHub blob URL into a GitHub raw URL.

    Example:
    https://github.com/user/repository/blob/main/data/test.csv

    Becomes:
    https://raw.githubusercontent.com/user/repository/main/data/test.csv
    """

    pattern = (
        r"https?://github\.com/"
        r"([^/]+)/([^/]+)/blob/([^/]+)/(.*)"
    )

    match = re.match(pattern, source)

    if match:
        owner, repository, branch, file_path = match.groups()

        return (
            f"https://raw.githubusercontent.com/"
            f"{owner}/{repository}/{branch}/{file_path}"
        )

    return source


def normalize_source(source):
    """
    Cleans local paths and converts GitHub blob URLs to raw URLs.
    """

    source = source.strip().strip('"').strip("'")

    if is_url(source):
        return convert_github_url_to_raw(source)

    return str(Path(source).expanduser())


def get_file_extension(source):
    """
    Gets the file extension from a local path or URL.
    """

    if is_url(source):
        parsed_url = urlparse(source)
        file_path = unquote(parsed_url.path)
        return Path(file_path).suffix.lower()

    return Path(source).suffix.lower()


def get_file_name(source):
    """
    Gets the file name without extension.
    Used as the SQLite table name for CSV files.
    """

    if is_url(source):
        parsed_url = urlparse(source)
        file_path = unquote(parsed_url.path)
        return Path(file_path).stem

    return Path(source).stem


# ---------------------------------------------------------
# Data loading functions
# ---------------------------------------------------------

def add_dataframe_to_sqlite(
    conn,
    df,
    table_name,
    original_source
):
    """
    Cleans a DataFrame and stores it in SQLite.
    """

    table_name = clean_identifier(
        table_name,
        default_name="Data"
    )

    df = df.copy()

    # Clean and uniquely rename columns.
    df.columns = make_unique_names(df.columns)

    # Store DataFrame inside SQLite.
    df.to_sql(
        table_name,
        conn,
        index=False,
        if_exists="replace"
    )

    table_details = {
        "original_source": original_source,
        "columns": list(df.columns),
        "data_types": {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        },
        "sample_rows": df.head(3).to_dict(
            orient="records"
        )
    }

    return table_name, table_details


def load_csv_to_sqlite(source, conn):
    """
    Loads a CSV file into one SQLite table.
    """

    try:
        df = pd.read_csv(source)
    except UnicodeDecodeError:
        # Fallback for CSV files using another encoding.
        df = pd.read_csv(source, encoding="latin1")

    table_name = get_file_name(source)

    table_name, table_details = add_dataframe_to_sqlite(
        conn=conn,
        df=df,
        table_name=table_name,
        original_source=source
    )

    return {
        table_name: table_details
    }


def load_excel_to_sqlite(source, conn):
    """
    Loads all Excel sheets into separate SQLite tables.
    """

    excel_data = pd.read_excel(
        source,
        sheet_name=None
    )

    table_info = {}
    used_table_names = set()

    for sheet_name, df in excel_data.items():
        base_table_name = clean_identifier(
            sheet_name,
            default_name="Sheet"
        )

        table_name = base_table_name
        count = 2

        # Prevent duplicate table names after cleaning.
        while table_name in used_table_names:
            table_name = f"{base_table_name}_{count}"
            count += 1

        used_table_names.add(table_name)

        table_name, table_details = add_dataframe_to_sqlite(
            conn=conn,
            df=df,
            table_name=table_name,
            original_source=sheet_name
        )

        table_info[table_name] = table_details

    return table_info


def load_file_to_sqlite(source):
    """
    Detects the file type and loads CSV or Excel into SQLite.
    """

    source = normalize_source(source)
    extension = get_file_extension(source)

    supported_extensions = {
        ".csv",
        ".xlsx",
        ".xlsm",
        ".xls"
    }

    if extension not in supported_extensions:
        raise ValueError(
            "Unsupported file format. "
            "Please provide a CSV, XLSX, XLSM, or XLS file."
        )

    # Verify a local file exists.
    if not is_url(source):
        if not Path(source).exists():
            raise FileNotFoundError(
                f"File not found: {source}"
            )

    conn = sqlite3.connect(":memory:")

    try:
        if extension == ".csv":
            table_info = load_csv_to_sqlite(
                source,
                conn
            )
        else:
            table_info = load_excel_to_sqlite(
                source,
                conn
            )

        if not table_info:
            raise ValueError(
                "The file does not contain readable data."
            )

        return conn, table_info, source

    except Exception:
        conn.close()
        raise


# ---------------------------------------------------------
# User file selection
# ---------------------------------------------------------

def choose_data_source(current_source):
    """
    Asks whether the user wants the current/default file
    or another local file/URL.
    """

    print("\nCurrent/default file:")
    print(current_source)

    answer = input(
        "\nDo you want to use this file? (yes/no): "
    ).strip().lower()

    if answer in {"", "yes", "y"}:
        return current_source

    new_source = input(
        "\nEnter local Excel/CSV path or GitHub raw URL:\n"
    ).strip()

    if not new_source:
        print("No new path provided. Using the current file.")
        return current_source

    return new_source


def display_tables(table_info):
    """
    Displays available SQLite tables and columns.
    """

    print("\nAvailable tables:")

    for table_name, info in table_info.items():
        print(f"\nTable: {table_name}")
        print(
            "Columns:",
            ", ".join(info["columns"])
        )


# ---------------------------------------------------------
# LLM SQL generation
# ---------------------------------------------------------

def ask_ollama_for_sql(question, table_info):
    schema_text = ""

    for table_name, info in table_info.items():
        schema_text += f"\nTable: {table_name}\n"

        schema_text += (
            f"Columns: {', '.join(info['columns'])}\n"
        )

        schema_text += (
            f"Column data types: {info['data_types']}\n"
        )

        schema_text += (
            f"Sample rows: {info['sample_rows']}\n"
        )

    prompt = f"""
You are an expert data analyst.

The user has loaded an Excel or CSV file into SQLite tables.

Database schema:
{schema_text}

User question:
{question}

Write exactly one valid SQLite SELECT query that answers
the user's question.

Rules:
- Return only the SQL query.
- Do not explain the query.
- Do not use markdown or code blocks.
- Use only the tables and columns given in the schema.
- Never invent table names or column names.
- Use SQLite syntax.
- Use SQL aggregation for count, sum, average, maximum,
  minimum and grouped calculations.
- Use AVG() for average calculations.
- Use COUNT() for counting rows.
- The query must be read-only.
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You convert natural-language data "
                    "questions into valid read-only SQLite SQL."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    sql = response["message"]["content"].strip()

    sql = (
        sql.replace("```sql", "")
        .replace("```SQL", "")
        .replace("```", "")
        .strip()
    )

    return sql


# ---------------------------------------------------------
# SQL validation and execution
# ---------------------------------------------------------

def validate_sql(sql):
    """
    Allows only read-only SELECT or WITH queries.
    """

    sql = sql.strip()

    if not sql:
        raise ValueError(
            "The model returned an empty SQL query."
        )

    # Remove one trailing semicolon.
    sql_without_end_semicolon = sql.rstrip(";").strip()

    if ";" in sql_without_end_semicolon:
        raise ValueError(
            "Multiple SQL statements are not allowed."
        )

    if not re.match(
        r"^(SELECT|WITH)\b",
        sql_without_end_semicolon,
        flags=re.IGNORECASE
    ):
        raise ValueError(
            "Only SELECT queries are allowed."
        )

    forbidden_keywords = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "CREATE",
        "REPLACE",
        "ATTACH",
        "DETACH",
        "PRAGMA"
    ]

    forbidden_pattern = (
        r"\b("
        + "|".join(forbidden_keywords)
        + r")\b"
    )

    if re.search(
        forbidden_pattern,
        sql_without_end_semicolon,
        flags=re.IGNORECASE
    ):
        raise ValueError(
            "The generated SQL contains a forbidden operation."
        )

    return sql_without_end_semicolon


def execute_sql(conn, sql):
    try:
        safe_sql = validate_sql(sql)

        result = pd.read_sql_query(
            safe_sql,
            conn
        )

        return result, None

    except Exception as error:
        return None, str(error)


# ---------------------------------------------------------
# Result explanation
# ---------------------------------------------------------

def explain_result(question, sql, result_df):
    if result_df.empty:
        return (
            "No matching records were found for the question."
        )

    result_text = result_df.to_markdown(index=False)

    prompt = f"""
The user asked:
{question}

SQL query used:
{sql}

SQL result:
{result_text}

Give a clear and simple answer based only on the SQL result.

Rules:
- Do not add assumptions.
- Do not change the values.
- Mention units such as salary or percentage only if the
  question or result provides that information.
- Keep the answer concise.
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You explain database query results "
                    "accurately and simply."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()


# ---------------------------------------------------------
# Load or change data source
# ---------------------------------------------------------

def load_selected_source(source):
    """
    Loads a selected source and prints its information.
    """

    print("\nLoading data source...")
    print(source)

    conn, table_info, normalized_source = (
        load_file_to_sqlite(source)
    )

    print("\nFile loaded successfully.")
    print("Source:", normalized_source)

    display_tables(table_info)

    return conn, table_info, normalized_source


def change_data_source(
    current_conn,
    current_source
):
    """
    Lets the user change the file without restarting
    the program.
    """

    new_source = input(
        "\nEnter another local Excel/CSV path "
        "or GitHub raw URL:\n"
    ).strip()

    if not new_source:
        print("No file path was entered.")
        return current_conn, None, current_source

    try:
        # Load the new source before closing the old one.
        new_conn, new_table_info, normalized_source = (
            load_selected_source(new_source)
        )

        current_conn.close()

        return (
            new_conn,
            new_table_info,
            normalized_source
        )

    except Exception as error:
        print("\nUnable to load the new file:")
        print(error)
        print("\nContinuing with the current file.")

        return current_conn, None, current_source


# ---------------------------------------------------------
# Main program
# ---------------------------------------------------------

def main():
    print("=" * 60)
    print("Excel/CSV AI Data Analyst")
    print("=" * 60)

    selected_source = choose_data_source(
        DEFAULT_FILE
    )

    # Keep asking until a valid initial source is loaded
    # or the user exits.
    while True:
        try:
            conn, table_info, current_source = (
                load_selected_source(selected_source)
            )
            break

        except Exception as error:
            print("\nUnable to load the file:")
            print(error)

            selected_source = input(
                "\nEnter another Excel/CSV path or URL, "
                "or type 'exit':\n"
            ).strip()

            if selected_source.lower() in {
                "exit",
                "quit"
            }:
                return

    print("\nCommands:")
    print("- Ask any question about the data")
    print("- Type 'tables' to display tables and columns")
    print("- Type 'change' to select another file")
    print("- Type 'exit' to close the program")

    while True:
        question = input(
            "\nAsk a question about the file: "
        ).strip()

        if not question:
            continue

        command = question.lower()

        if command in {"exit", "quit"}:
            print("\nClosing the program.")
            conn.close()
            break

        if command == "tables":
            display_tables(table_info)
            continue

        if command in {
            "change",
            "change file",
            "switch",
            "switch file"
        }:
            new_conn, new_table_info, new_source = (
                change_data_source(
                    current_conn=conn,
                    current_source=current_source
                )
            )

            conn = new_conn
            current_source = new_source

            if new_table_info is not None:
                table_info = new_table_info

            continue

        try:
            sql = ask_ollama_for_sql(
                question,
                table_info
            )

            print("\nGenerated SQL:")
            print(sql)

            result_df, error = execute_sql(
                conn,
                sql
            )

            if error:
                print("\nError while running SQL:")
                print(error)
                continue

            print("\nSQL Result:")
            print(result_df.to_string(index=False))

            final_answer = explain_result(
                question,
                sql,
                result_df
            )

            print("\nAnswer:")
            print(final_answer)

        except Exception as error:
            print("\nAn unexpected error occurred:")
            print(error)


if __name__ == "__main__":
    main()