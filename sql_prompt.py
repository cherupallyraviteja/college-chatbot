DB_SCHEMA = """
Tables:

students(id, roll_no, name, year, semester, department, cgpa, fee_status, password, attendance)
faculty(id, name, designation, qualification, jntuh_id, aicte_id, institution_id, email, conferences, patents)
fee_details(id, program, fee_category, amount)
admission_programs(program_id, degree_program, duration_years, total_intake, a_category_intake, b_category_intake)
admission_process(id, program_type, description)
admission_documents(document_id, document_name, ap_ts_students_required, national_students_required)
transport_details(route_id, route_no, driver_name, driver_phone, bus_number)
route_pickup_points(id, route_id, pickup_point, pickup_time, stop_order)
placements(id, academic_year, roll_no, student_name, branch, company)

"""

SCHEMA = {
    "students": """
TABLE: students
COLUMNS:
id
roll_no
name
year
semester
department
cgpa
fee_status
password
attendance
""",

    "faculty": """
TABLE: faculty
COLUMNS:
id
name
designation
qualification
jntuh_id
aicte_id
institution_id
email
conferences
patents
department
""",

    "fee_details": """
TABLE: fee_details
COLUMNS:
id
program
fee_category
amount
""",

    "degree_programs": """
TABLE: admission_programs
COLUMNS:
program_id
degree_program
duration_years
total_intake
a_category_intake
b_category_intake
""",

    "admission_process": """
TABLE: admission_process
COLUMNS:
id
program
description
""",

    "admission_documents": """
TABLE: admission_documents
COLUMNS:
document_id
document_name
ap_ts_students_required
national_students_required
""",

    "transport_details": """
TABLE: transport_details
COLUMNS:
route_id
route_no
driver_name
driver_phone
bus_number
""",

    "route_pickup_points": """
TABLE: route_pickup_points
COLUMNS:
id
route_no
pickup_point
pickup_time
stop_order
""",

    "placements": """
TABLE: placements
COLUMNS:
id
academic_year
roll_no
student_name
branch
company
"""
}

from entity_extractor import extract_entities
from schema_semantics import get_column_metadata
from sql_generator import generate_sql
from table_router import route_tables
from schema_semantics import TABLE_SEMANTICS


def build_sql_prompt(user_query: str, tables: list[str]) -> str:
    metadata = get_column_metadata(tables)

    schema_text = ""

    for table in tables:
        schema_text += f"\nTABLE: {table}\n"
        examples =""
        for col in metadata[table]:
            if table != "admission_process":
                examples = ", ".join(col["examples"]) if col["examples"] else "N/A"
            meaning = TABLE_SEMANTICS[table].get(col['column'], "")

            schema_text += (
                f"{col['column']} ({col['type']})\n"
                f"  - meaning: {meaning}\n"
                f"  - usage: {col['usage']}\n"
                f"  - examples: {examples}\n"
            )

    entity_text = ""
    entities = extract_entities(user_query)
    if entities:
        entity_text += "\nEXTRACTED ENTITIES:\n"
        for k, v in entities.items():
            entity_text += f"- {k}: {v}\n"

    extra_rules = """
    IMPORTANT SEMANTICS:
    - designation refers to roles like Professor, Assistant Professor
    - fee_status refers to values like Paid, Pending
    - roll_no is unique identifier, always use exact match
    - names should be matched using ILIKE for flexibility

    FUZZY MATCHING RULES:
    - For name columns → use trigram similarity
    - Use: column % 'value'
    - Do NOT use '=' for names
    - Use ORDER BY similarity(column, 'value') DESC for best match
    """
    
    return f"""
    You are an expert PostgreSQL SQL generator.

    STRICT RULES:
    - Use PostgreSQL syntax only
    - Never use backticks (`) for identifiers
    - Output ONLY SQL
    - No explanation
    - Use only the given table
    - Always end with semicolon

    SQL CAPABILITY CONSTRAINT:

    This system supports ONLY simple single-table queries.

    OUTPUT FORMAT (STRICT):
    SELECT [columns]
    FROM [table]
    WHERE [conditions];

    RULES:
    - Use only ONE table
    - Do NOT use JOIN
    - Do NOT use subqueries
    - Prefer simple filtering conditions

    NAME MATCHING RULE:
    - For name columns, ALWAYS use trigram similarity operator (%)
    - Do NOT use '=' or ILIKE for names

    TEXT MATCHING RULE:
    - For text columns, ALWAYS use ILIKE or LOWER()
    - NEVER use '=' for text comparison

    If the query requires unsupported operations (JOIN, aggregation, etc.),
    return:
    SELECT 'NOT_SUPPORTED';

    COLUMN SELECTION RULE:
    - Choose only relevant columns
    - If question asks "which X", return identifier column of X
    - Use DISTINCT when returning identifiers

    IMPORTANT:
    - For roll_no → exact match
    - For numeric → use comparison operators

    ---

    SCHEMA:
    {schema_text}

    ---

    {extra_rules}

    ---

    {entity_text}

    ---

    QUESTION:
    {user_query}

    SQL:
    
    """
if __name__ == "__main__":
    while True:
        query = input("Enter your query: ")
        if query.lower() == "exit":
            break
        tables = route_tables(query)
        entities = extract_entities(query)

        # ---- FORCE LOGIC FOR NAME ----
        if "name" in entities and tables:
            name = entities["name"]
            table = tables[0]

            sql = f"""
            SELECT *
            FROM {table}
            WHERE REPLACE(name, '.', '') % '{name}'
            ORDER BY similarity(REPLACE(name, '.', ''), '{name}') DESC;
            """

        else:
        # normal flow
            prompt = build_sql_prompt(query, tables)
            sql=generate_sql(prompt) 
            print("Prompt:", prompt)
            # assume this function exists
        print("SQL:", sql)
        print()