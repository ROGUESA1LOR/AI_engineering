from fastapi import Fastapi

app=Fastapi()
@app.get("/health")
def health_check():
    return {"status": "ok"}
