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
route_id
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

from schema_semantics import get_column_metadata
from sql_generator import generate_sql
from table_router import route_tables

def build_sql_prompt(user_query: str, tables: list[str]) -> str:
    metadata = get_column_metadata(tables)

    schema_text = ""

    for table in tables:
        schema_text += f"\nTABLE: {table}\n"

        for col in metadata[table]:
            examples = ", ".join(col["examples"]) if col["examples"] else "N/A"

            schema_text += (
                f"{col['column']} ({col['type']})\n"
                f"  - usage: {col['usage']}\n"
                f"  - examples: {examples}\n"
            )
    extra_rules = """
    IMPORTANT SEMANTICS:
    - designation refers to roles like Professor, Assistant Professor
    - fee_status refers to values like Paid, Pending
    - roll_no is unique identifier, always use exact match
    - names should be matched using ILIKE for flexibility
    """ 
    return f"""
    You are an expert PostgreSQL SQL generator.

    STRICT RULES:
    - Output ONLY SQL
    - No explanation
    - Use only given tables
    - Always end with semicolon

    IMPORTANT:
    - Use examples to infer correct filters
    - If query mentions a value similar to examples, use exact match
    - For names → use ILIKE
    - For roll_no → exact match
    - For text → use LOWER() or ILIKE
    - For numeric → use comparison operators

    ---

    SCHEMA:
    {schema_text}

    ---

    {extra_rules}

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
        prompt = build_sql_prompt(query, tables)
        sql=generate_sql(prompt)  # assume this function exists
        print("SQL:", sql)
        print()