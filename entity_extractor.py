import re

def normalize_name(text):
    return text.replace(".", " ").strip()

def extract_entities(query: str):
    entities = {}

    # ---- Roll number ----
    roll_match = re.search(r'\b\d{2}[A-Za-z]\d[A-Za-z]\d{4}\b', query)
    if roll_match:
        entities["roll_no"] = roll_match.group()

    # ---- Numbers ----
    numbers = re.findall(r'\b\d+\b', query)
    if numbers:
        entities["numbers"] = numbers

    # ---- Name (simple heuristic) ----
    words = query.split()
    name_parts = [w for w in words if w[0].isupper()]
    
    if len(name_parts) >= 2:
        entities["name"] = " ".join(name_parts)
        entities["name"] = normalize_name(entities["name"])

    return entities