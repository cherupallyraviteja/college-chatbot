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


def build_sql_prompt(user_query, tables):
    schema_text = "\n".join(SCHEMA[t] for t in tables)

    return f"""
You are a PostgreSQL SQL generator.

STRICT RULES:
- Output ONLY SQL
- No markdown, no explanation
- Use ONLY the schema below
- Do NOT use tables not shown
- Do NOT invent columns
- Values for roll_no must always be enclosed in single quotes
JOIN RULE:
- route_pickup_points can only be joined with transport_details using route_id

- If not answerable, output:
  SELECT 'NOT_SUPPORTED' AS message;

SCHEMA:
{schema_text}

QUESTION:
{user_query}

SQL:"""

"""
from schema_semantics import TABLE_SEMANTICS

def build_sql_prompt(user_query: str, tables: list[str]) -> str:
    schema_blocks = []

    for table in tables:
        schema_blocks.append(SCHEMA[table])

        semantics = TABLE_SEMANTICS.get(table, {})
        if semantics:
            semantic_text = "\n".join(
                f"- {col}: {desc}"
                for col, desc in semantics.items()
            )
            schema_blocks.append(
                f"COLUMN MEANINGS:\n{semantic_text}"
            )

    schema_text = "\n\n".join(schema_blocks)

    return f""
You are a PostgreSQL SQL generator.

STRICT RULES:
- Output ONLY SQL
- No markdown, no explanation
- Use ONLY the schema below
- Do NOT use tables not shown
- Do NOT invent columns
- Values for roll_no must always be enclosed in single quotes
JOIN RULE:
- route_pickup_points can only be joined with transport_details using route_id

- If not answerable, output:
  SELECT 'NOT_SUPPORTED' AS message;
SCHEMA:
{schema_text}

QUESTION:
{user_query}

SQL:
"""
