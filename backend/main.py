from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from query_engine import text_to_sql, execute_query
 # This import now works!
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(q: Question):
    sql = text_to_sql(q.question)
    result = execute_query(sql)

    print("\n[User Question]:", q.question)
    print("[Generated SQL]:", sql)

    if "error" in result:
        print("[SQL Error]:", result["error"])
        return {"error": result["error"], "sql": sql}
    
    print("[SQL Result]:")
    for row in result["rows"]:
        print(row)

    return {"sql": sql, "result": result}

