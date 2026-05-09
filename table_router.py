from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    local_files_only=True
)

TABLE_DESCRIPTIONS = {
    "students": "student details like name roll cgpa attendance",
    "faculty": "faculty teachers professors designation qualification",
    "fee_details": "fees payment amount structure",
    "degree_programs": "courses programs duration intake",
    "admission_process": "admission steps procedure",
    "admission_documents": "documents certificates required",
    "transport_details": "bus routes driver transport",
    "route_pickup_points": "bus stops pickup timings",
    "placements": "jobs companies placements students",
}

COLUMN_DESCRIPTIONS = {
    # students
    "students.roll_no": "unique student roll number identifier",
    "students.name": "student full name",
    "students.cgpa": "numeric cgpa score of a student",
    "students.attendance": "student attendance percentage",
    "students.fee_status": "student fee payment status paid or pending",

    # faculty
    "faculty.name": "faculty member name teacher professor",
    "faculty.designation": "faculty role professor assistant professor hod",
    "faculty.department": "faculty department",

    # transport
    "transport_details.route_no": "Public-facing route number.",
    "transport_details.driver_name": "Name of the driver.",
    "transport_details.driver_phone": "Contact phone number of the driver.",
    "transport_details.bus_number": "Registration number of the bus.",

    # route_pickup_points
    "route_pickup_points.route_no": "Public-facing route number.",
    "route_pickup_points.pickup_point": "Name of a particular bus stop or pickup point",
    "route_pickup_points.pickup_time": "Scheduled pickup time.",
    "route_pickup_points.stop_order": "Sequence order of the stop on the route.",


    # placements
    "placements.company": "company name placement",
    "placements.student_name": "placed student name",
    "placements.academic_year": "Academic year of placement.",
    "placements.roll_no": "Roll number of the placed student.",
    "placements.branch": "Academic branch of the student.",

    # admission documents
    "admission_documents.document_name": "Name of the document required for admission",
    "admission_documents.document_id": "Internal numeric identifier for a document record.",
    "admission_documents.ap_ts_students_required": "Whether required for AP/TS students.",
    "admission_documents.national_students_required": "Whether required for non-AP/TS students.",
    
    #admission process
    "admission_process.program": "Academic program name for which the admission applies.",
    "admission_process.description": "Description explaining the admission procedure.",

    # fees
    "fee_details.amount": "Monetary amount charged for the fee category.",
    "fee_details.program": "Academic program to which the fee applies.",
    "fee_details.fee_category": "Category or type of fee.",

    # programs
    "degree_programs.degree_program": "Name of the degree program.",
}

def get_table(col):
    return col.split(".")[0]

# Precompute embeddings
column_embeddings = {
    col: model.encode(desc, convert_to_tensor=True)
    for col, desc in COLUMN_DESCRIPTIONS.items()
}

def route_tables(user_query: str, top_k_tables=3):
    query_emb = model.encode(user_query, convert_to_tensor=True)

    col_scores = []
    for col, emb in column_embeddings.items():
        score = util.cos_sim(query_emb, emb).item()
        col_scores.append((col, score))

    col_scores.sort(key=lambda x: x[1], reverse=True)

    # ---- aggregate table scores ----
    table_scores = {}
    for col, score in col_scores[:8]:   # slightly more columns
        table = get_table(col)
        table_scores[table] = table_scores.get(table, 0) + score

    # ---- normalize (important) ----
    for table in table_scores:
        table_scores[table] /= 8

    # ---- rank ----
    ranked = sorted(table_scores.items(), key=lambda x: x[1], reverse=True)

    # ---- dynamic filtering (key fix) ----
    selected = []
    if not ranked:
        return []

    print("Selected Tables : ",ranked[0][0])

    return [ranked[0][0]]  # always include best

    return selected
if __name__ == "__main__":
    while True:
        query = input("Enter your query: ")
        if query.lower() == "exit":
            break
        tables = route_tables(query)
        print("Relevant tables:", tables)
        print()