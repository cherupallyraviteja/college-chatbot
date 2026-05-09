# schema_semantics.py

TABLE_SEMANTICS = {
    "students": {
        "id": "Internal numeric identifier for a student record, used only by the database.",
        "roll_no": "Official alphanumeric roll number that uniquely identifies a student.",
        "name": "Full name of the student.",
        "year": "Current academic year of the student in the program.",
        "semester": "Current semester number of the student.",
        "department": "Academic department in which the student is enrolled.",
        "cgpa": "Cumulative Grade Point Average representing academic performance.",
        "fee_status": "Indicates whether the student’s fees are paid or pending.",
        "password": "Authentication credential for the student account, stored in hashed form.",
        "attendance": "Attendance percentage or attendance score of the student."
    },
    "faculty": {
        "id": "Internal numeric identifier for a faculty record.",
        "name": "Full name of the faculty member.",
        "designation": "Official role or designation of the faculty member.",
        "qualification": "Educational qualifications of the faculty member.",
        "jntuh_id": "JNTUH registration or identification number of the faculty member.",
        "aicte_id": "AICTE registration or identification number of the faculty member.",
        "institution_id": "Internal institution-specific identifier for the faculty member.",
        "email": "Official email address of the faculty member.",
        "conferences": "Details or count of conferences attended or published.",
        "patents": "Details or count of patents filed or granted.",
        "department": "Academic department to which the faculty member belongs."
    },
    "fee_details": {
        "id": "Internal numeric identifier for a fee record.",
        "program": "Academic program to which the fee applies.",
        "fee_category": "Category or type of fee.",
        "amount": "Monetary amount charged for the fee category."
    },
    "degree_programs": {
        "program_id": "Internal identifier for the degree or academic program.",
        "degree_program": "Name of the degree or academic program.",
        "duration_years": "Total duration of the program in years.",
        "total_intake": "Total number of seats available.",
        "a_category_intake": "Seats allocated under A-category.",
        "b_category_intake": "Seats allocated under B-category."
    },
    "admission_process": {
        "id": "Internal numeric identifier for an admission process record.",
        "program": "Academic program for which the admission applies.",
        "description": "Description explaining the admission procedure."
    },
    "admission_documents": {
        "document_id": "Internal numeric identifier for a document record.",
        "document_name": "Name of the document required.",
        "ap_ts_students_required": "Whether required for AP/TS students.",
        "national_students_required": "Whether required for non-AP/TS students."
    },
    "transport_details": {
        "route_id": "Internal identifier for a transport route.",
        "route_no": "Public-facing route number.",
        "driver_name": "Name of the driver.",
        "driver_phone": "Contact phone number of the driver.",
        "bus_number": "Registration number of the bus."
    },
    "route_pickup_points": {
        "id": "Internal numeric identifier for a pickup point.",
        "route_no": "Identifier of the related transport route.",
        "pickup_point": "Name of the pickup location.",
        "pickup_time": "Scheduled pickup time.",
        "stop_order": "Sequence order of the stop on the route."
    },
    "placements": {
        "id": "Internal numeric identifier for a placement record.",
        "academic_year": "Academic year of placement.",
        "roll_no": "Roll number of the placed student.",
        "student_name": "Name of the placed student.",
        "branch": "Academic branch of the student.",
        "company": "Company where the student was placed."
    }
}
import psycopg2
from config import DB_CONFIG

def get_column_metadata(tables: list[str]):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    metadata = {}

    for table in tables:
        cur.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = %s;
        """, (table,))

        columns = cur.fetchall()
        metadata[table] = []

        for col, dtype in columns:
            # ---- Detect type ----
            if dtype in ["integer", "numeric", "real", "double precision"]:
                col_type = "numeric"
                usage = "use >, <, = for comparison"

            elif "char" in dtype or "text" in dtype:
                col_type = "text"
                usage = "use LOWER() or ILIKE for comparison"

            else:
                col_type = dtype
                usage = "use appropriate comparison"

            # ---- Fetch sample values (NEW PART) ----
            sample_values = []
            try:
                cur.execute(f"""
                    SELECT {col}
                    FROM {table}
                    WHERE {col} IS NOT NULL
                    LIMIT 3;
                """)
                sample_values = [str(r[0]) for r in cur.fetchall()]
            except:
                pass  # ignore errors (like large fields)

            metadata[table].append({
                "column": col,
                "type": col_type,
                "usage": usage,
                "examples": sample_values
            })

    cur.close()
    conn.close()
    return metadata
