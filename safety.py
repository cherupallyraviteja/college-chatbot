import re

FORBIDDEN_KEYWORDS = {
    "insert", "update", "delete", "drop", "alter",
    "--", "/*", "*/"
}

def validate_and_clean_sql(raw_sql: str):
    """
    Returns (is_valid: bool, cleaned_sql: str)
    """

    if not raw_sql:
        return False, ""

    # 1️⃣ Remove markdown/code fences
    sql = re.sub(r"```sql|```", "", raw_sql, flags=re.IGNORECASE).strip()

    sql_l = sql.lower()

    # 2️⃣ Must start with SELECT
    if not sql_l.startswith("select"):
        return False, sql

    # 3️⃣ Block dangerous keywords
    for kw in FORBIDDEN_KEYWORDS:
        if kw in sql_l:
            return False, sql

    # 4️⃣ Basic sanity check
    if ";" not in sql:
        return False, sql

    return True, sql
