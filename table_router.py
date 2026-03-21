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
    "transport_details.route_no": "bus route number",
    "transport_details.driver_name": "bus driver name",
    "route_pickup_points.pickup_point": "bus stop location",
    "route_pickup_points.pickup_time": "bus pickup timing",

    # placements
    "placements.company": "company name placement",
    "placements.student_name": "placed student name",

    # admission
    "admission_documents.document_name": "required documents certificates",
    "admission_process.description": "admission procedure",

    # fees
    "fee_details.amount": "fee amount",
    "fee_details.program": "program fee structure",
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