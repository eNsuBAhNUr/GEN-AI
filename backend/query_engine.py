import sqlite3
from difflib import get_close_matches

def connect_db():
    return sqlite3.connect("ecpm.db")

def get_schema():
    conn = connect_db()
    cursor = conn.cursor()
    schema = {}
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for (table_name,) in tables:
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            schema[table_name] = [col[1] for col in columns]
    finally:
        conn.close()
    return schema

def text_to_sql(user_input: str) -> str:
    user_input = user_input.lower().strip()
    schema = get_schema()

    mapping = {
        "what is my total sales": "SELECT SUM(total_sales) FROM total_sales;",
        "calculate the roas": "SELECT SUM(ad_sales) * 1.0 / NULLIF(SUM(ad_spend), 0) AS RoAS FROM ad_sales;",
        "which product had the highest cpc": "SELECT item_id, ad_spend * 1.0 / NULLIF(clicks, 0) AS cpc FROM ad_sales ORDER BY cpc DESC LIMIT 1;",
        "top selling product": "SELECT item_id, SUM(total_sales) AS total FROM total_sales GROUP BY item_id ORDER BY total DESC LIMIT 1;",
        "average ad spend": "SELECT AVG(ad_spend) FROM ad_sales;",
        "total ad sales": "SELECT SUM(ad_sales) FROM ad_sales;",
        "total units sold": "SELECT SUM(units_sold) FROM ad_sales;",
        "list all products": "SELECT DISTINCT item_id FROM total_sales;",
        "clicks by item": "SELECT item_id, COUNT(clicks) AS click_count FROM ad_sales GROUP BY item_id ORDER BY click_count DESC;",
        "total ad spend over time": "SELECT date, SUM(ad_spend) AS total_spend FROM ad_sales GROUP BY date ORDER BY date;",
        "impressions vs clicks per item": "SELECT item_id, SUM(impressions) AS total_impressions, SUM(clicks) AS total_clicks FROM ad_sales GROUP BY item_id ORDER BY total_impressions DESC;",
        "units sold per item": "SELECT item_id, SUM(units_sold) AS total_units FROM ad_sales GROUP BY item_id ORDER BY total_units DESC;",
        "top selling items": "SELECT item_id, SUM(total_sales) AS total FROM total_sales GROUP BY item_id ORDER BY total DESC;",
        "eligibility count by status": "SELECT eligibility, COUNT(*) AS count FROM eligibility GROUP BY eligibility;",
        "conversion rate per item": "SELECT item_id, SUM(units_sold) * 1.0 / NULLIF(SUM(clicks), 0) AS units_per_click FROM ad_sales GROUP BY item_id ORDER BY units_per_click DESC;"
    }

    match = get_close_matches(user_input, mapping.keys(), n=1, cutoff=0.6)
    if match:
        return mapping[match[0]]

    for table, columns in schema.items():
        for col in columns:
            if col in user_input:
                if "sum" in user_input or "total" in user_input:
                    return f"SELECT SUM({col}) FROM {table};"
                elif "average" in user_input or "avg" in user_input:
                    return f"SELECT AVG({col}) FROM {table};"
                elif "max" in user_input or "highest" in user_input:
                    return f"SELECT MAX({col}) FROM {table};"
                elif "list" in user_input or "show" in user_input:
                    return f"SELECT DISTINCT {col} FROM {table};"
                elif "count" in user_input:
                    return f"SELECT {col}, COUNT(*) as count FROM {table} GROUP BY {col} ORDER BY count DESC;"

    return ""

def execute_query(sql: str):
    if not sql.strip():
        return {"error": "Empty or unrecognized query."}

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return {"columns": columns, "rows": rows}
    except Exception as e:
        return {"error": f"SQL Error: {str(e)}"}
    finally:
        conn.close()
