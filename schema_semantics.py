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
        "route_id": "Identifier of the related transport route.",
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
