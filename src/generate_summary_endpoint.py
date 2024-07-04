# generate_summary_endpoint.py
from fastapi import FastAPI, HTTPException
from llama3_integration import generate_summary

app = FastAPI()

@app.post("/generate-summary")
async def generate_summary_endpoint(content: str):
    try:
        summary = generate_summary(content)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
