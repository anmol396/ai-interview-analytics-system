from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.services.ai_classifier import classify_query, COLUMN_MAP

def format_markdown_table(rows, headers=["Rank", "Name", "Role", "Status", "Score"]):
    if not rows: return "No candidates found."
    table = f"| {' | '.join(headers)} |\n| {' | '.join(['---'] * len(headers))} |\n"
    for i, row in enumerate(rows):
        name = row[1].replace("_", " ") if len(row) > 1 else "Unknown"
        role = row[2] if len(row) > 2 else "Unknown"
        status = row[3] if len(row) > 3 else "Unknown"
        score = row[4] if len(row) > 4 else 0
        table += f"| {i+1} | {name} | {role} | {status} | {score} |\n"
    return table

def handle_query_with_sql(query: str, db: Session) -> dict:
    params = classify_query(query)
    intent = params.get("intent")
    
    result = {
        "response": "", "type": intent, "title": "HR Analytics Result",
        "data": [], "insights": [], "has_more": False, "total": 0, "filter_key": None
    }
    
    if intent == "OUT_OF_SCOPE":
        return {"response": "I'm designed to help with HR analytics. That topic is outside my current scope.", "title": "Outside HR Scope"}
    if intent == "GENERAL": return {"response": "TRIGGER_LLM"}

    if intent == "SUMMARY":
        row = db.execute(text("SELECT COUNT(*) as total, SUM(CASE WHEN LOWER(status) LIKE '%pass%' THEN 1 ELSE 0 END) as passed, SUM(CASE WHEN LOWER(status) LIKE '%fail%' THEN 1 ELSE 0 END) as failed, SUM(CASE WHEN LOWER(status) LIKE '%pending%' THEN 1 ELSE 0 END) as pending FROM hr_candidates")).fetchone()
        d = dict(row._mapping)
        result.update({"title": "Overall Performance Summary", "type": "summary", "data": d})
        resp = f"### {result['title']}\n| Metric | Value |\n| --- | --- |\n"
        resp += f"| Total Candidates | {d['total']} |\n| Passed | {d['passed']} |\n| Failed | {d['failed']} |\n| Pending | {d['pending']} |\n"
        result["response"] = resp
        return result

    if intent == "RECOMMENDATION":
        rows = db.execute(text("SELECT id, name, role, status, total_score FROM hr_candidates WHERE LOWER(status) LIKE '%pass%' ORDER BY total_score DESC LIMIT 5")).fetchall()
        result.update({"title": "Top Recommended Candidates", "type": "recommendation", "data": [dict(r._mapping) for r in rows]})
        if rows:
            names = [r[1].replace('_',' ') for r in rows if r[4] == rows[0][4]]
            result["insights"] = [f"Top Recommended: **{', '.join(names)}**"]
            result["response"] = f"### {result['title']}\n\n" + format_markdown_table(rows)
        else: result["response"] = "No passed candidates available."
        return result

    if intent == "PERFORMANCE":
        lim = params.get("limit", 5)
        rows = db.execute(text("SELECT id, name, role, status, total_score FROM hr_candidates ORDER BY total_score DESC LIMIT :lim"), {"lim": lim}).fetchall()
        result.update({"title": f"Top {lim} Performers", "data": [dict(r._mapping) for r in rows], "type": "top_candidates"})
        if rows:
            result["insights"] = [f"Highest scorer: **{rows[0][1].replace('_',' ')}**"]
            result["response"] = f"### {result['title']}\n\n" + format_markdown_table(rows)
        return result

    if intent == "COMPARE_TOP":
        role, limit = params.get("role"), params.get("limit", 2)
        rows = db.execute(text(
            "SELECT name, role, status, written_test, technical_assessment, pm_assessment, hr_evaluation, total_score "
            "FROM hr_candidates WHERE LOWER(role) LIKE :r ORDER BY total_score DESC LIMIT :lim"
        ), {"r": f"%{role.lower()}%", "lim": limit}).fetchall()
        if len(rows) < 2:
            result["response"] = f"Not enough {role}s found to compare top {limit}."
            return result
        names = [r[0] for r in rows]
        result["title"] = f"Top {limit} {role}s Comparison"
        resp = f"### {result['title']}:\n| Metric | {' | '.join(names)} |\n| --- | {' | '.join(['---'] * len(names))} |\n"
        metrics = [("Role", 1), ("Status", 2), ("Written", 3), ("Technical", 4), ("PM", 5), ("HR", 6), ("Total", 7)]
        for m, idx in metrics:
            resp += f"| {m} | {' | '.join(str(r[idx]) for r in rows)} |\n"
        result["response"] = resp
        return result

    if intent == "COMPARE":
        names, data = params.get("names", []), []
        for name in names:
            row = db.execute(text("SELECT name, role, status, written_test, technical_assessment, pm_assessment, hr_evaluation, total_score FROM hr_candidates WHERE LOWER(name) LIKE LOWER(:w) LIMIT 1"), {"w": f"%{'%'.join(name.split())}%"}).fetchone()
            if row: data.append(row)
        if len(data) < 2:
            result["response"] = f"Could not find both candidates. Found: {', '.join([r[0] for r in data]) if data else 'None'}"
            return result
        result["title"] = f"Comparison: {data[0][0]} vs {data[1][0]}"
        resp = f"### Comparison Breakdown:\n| Metric | {data[0][0]} | {data[1][0]} |\n| --- | --- | --- |\n"
        metrics = [("Role", 1), ("Status", 2), ("Written", 3), ("Technical", 4), ("PM", 5), ("HR", 6), ("Total", 7)]
        for m, i in metrics: resp += f"| {m} | {data[0][i]} | {data[1][i]} |\n"
        result["response"] = resp
        return result

    # Handle both general analytics and role-specific analytics
    if intent in ("ANALYTICS", "ROLE_ANALYTICS"):
        rows = db.execute(text("SELECT role, COUNT(*) as count FROM hr_candidates GROUP BY role ORDER BY count DESC")).fetchall()
        result.update({"title": "Role Distribution Analytics", "type": "analytics", "data": [dict(r._mapping) for r in rows]})
        if rows:
            resp = f"### {result['title']}:\n| Role | Count |\n| --- | --- |\n"
            for r in rows: resp += f"| {r[0]} | {r[1]} |\n"
            result["response"] = resp
        return result

    if intent == "COUNT":
        s, r = params.get("status"), params.get("role")
        sql = "SELECT COUNT(*) FROM hr_candidates WHERE 1=1"
        binds = {}
        if s: sql += " AND LOWER(status) LIKE :s"; binds["s"] = f"%{s}%"
        if r: sql += " AND LOWER(role) LIKE :r"; binds["r"] = f"%{r}%"
        count = db.execute(text(sql), binds).scalar()
        result.update({"title": "Record Count", "response": f"Total Candidates: {count}", "total": count, "type": "count"})
        return result

    if intent == "SINGLE_METRIC":
        m, name = params["metric"], params["name"]
        col = COLUMN_MAP[m]
        row = db.execute(text(f"SELECT name, {col} FROM hr_candidates WHERE LOWER(REPLACE(name, '_', ' ')) LIKE :w LIMIT 1"), {"w": f"%{'%'.join(name.split())}%"}).fetchone()
        if row:
            result.update({"title": f"{m.title()} lookup", "type": "single_metric", "response": f"### {m.title()} for {row[0]}\n# {row[1]}"})
        else: result["response"] = f"No {m} found for '{name}'."
        return result

    if intent == "ROUND_FILTER":
        col, op, val, metric = params["column"], params["op"], params["value"], params["metric"]
        if params.get("is_count"):
            count = db.execute(text(f"SELECT COUNT(*) FROM hr_candidates WHERE {col} {op} :v"), {"v": val}).scalar()
            result.update({"title": f"Count: {metric} {op} {val}", "response": f"Total Candidates: {count}", "total": count, "type": "count"})
            return result
        rows = db.execute(text(f"SELECT id, name, role, status, {col} as score FROM hr_candidates WHERE {col} {op} :v ORDER BY {col} {'DESC' if op=='>' else 'ASC'} LIMIT 5"), {"v": val}).fetchall()
        total = db.execute(text(f"SELECT COUNT(*) FROM hr_candidates WHERE {col} {op} :v"), {"v": val}).scalar()
        result.update({"title": f"Candidates with {metric} {op} {val}", "type": "filter", "total": total, "has_more": total > 5, "filter_key": f"score_{col}_{op}_{val}"})
        if rows: result["response"] = f"### {result['title']}\n" + format_markdown_table(rows)
        else: result["response"] = "No candidates match."
        return result

    if intent in ["STATUS", "FILTER"]:
        s_val, op, score = params.get("status"), params.get("op"), params.get("score")
        if intent == "STATUS":
            sql = "SELECT id, name, role, status, total_score FROM hr_candidates WHERE LOWER(status) LIKE :s ORDER BY total_score DESC LIMIT 5"
            cnt_sql = "SELECT COUNT(*) FROM hr_candidates WHERE LOWER(status) LIKE :s"
            b = {"s": f"%{s_val}%"}
            result.update({"title": f"Status: {s_val}", "filter_key": f"status_{s_val}"})
        else:
            sql = f"SELECT id, name, role, status, total_score FROM hr_candidates WHERE total_score {op} :sc ORDER BY total_score {'DESC' if op=='>' else 'ASC'} LIMIT 5"
            cnt_sql = f"SELECT COUNT(*) FROM hr_candidates WHERE total_score {op} :sc"
            b = {"sc": score}
            result.update({"title": f"Score {op} {score}", "filter_key": f"score_{op}_{score}"})
        rows, total = db.execute(text(sql), b).fetchall(), db.execute(text(cnt_sql), b).scalar()
        result.update({"type": "filter", "total": total, "has_more": total > 5})
        if rows: result["response"] = f"### {result['title']}\n" + format_markdown_table(rows)
        return result

    if intent == "ROLE":
        role, lim = params["role"], params.get("limit", 5)
        rows = db.execute(text("SELECT id, name, role, status, total_score FROM hr_candidates WHERE LOWER(role) LIKE :r ORDER BY total_score DESC LIMIT :lim"), {"r": f"%{role.lower()}%", "lim": lim}).fetchall()
        total = db.execute(text("SELECT COUNT(*) FROM hr_candidates WHERE LOWER(role) LIKE :r"), {"r": f"%{role.lower()}%"}).scalar()
        result.update({"title": f"Top {role}s", "type": "role_query", "total": total, "has_more": total > lim, "filter_key": f"role_{role}"})
        if rows: result["response"] = f"### {result['title']}:\n" + format_markdown_table(rows)
        else: result["response"] = "No candidates found."
        return result

    if intent == "NAME":
        name = params["name"]
        row = db.execute(text("SELECT id, name, role, status, written_test, technical_assessment, pm_assessment, hr_evaluation, total_score FROM hr_candidates WHERE LOWER(REPLACE(name, '_', ' ')) LIKE :w LIMIT 1"), {"w": f"%{'%'.join(name.split())}%"}).fetchone()
        if row:
            result.update({"type": "candidate_detail", "title": f"Profile: {row[1]}", "response": f"### Summary for {row[1]}\n| Role | {row[2]} |\n| Status | {row[3]} |\n| Total Score | {row[8]} |"})
        else: result["response"] = "Candidate not found."
        return result

    return {"response": "Query could not be processed."}
