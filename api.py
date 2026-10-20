from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import re
from datetime import datetime

app = FastAPI(title="FinGPT-Omni - Patent mdsubhanpasha")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def smart_parse(txn: str):
    amt = re.search(r'\$?(\d+)', txn)
    amount = int(amt.group(1)) if amt else 0
    t_type = "CREDIT" if "CREDIT" in txn.upper() or "CLIENT" in txn.upper() else "DEBIT"
    merchant = "STARBUCKS" if "STARBUCKS" in txn.upper() else "DELTA AIR" if "DELTA" in txn.upper() else "GOOGLE"
    account = "Meals" if "STARBUCKS" in txn.upper() or "MEALS" in txn.upper() else "Travel" if "DELTA" in txn.upper() else "Office Expenses"
    if "CLIENT" in txn.upper(): account = "Client Income"
    return {"account": account, "amount": amount, "merchant": merchant, "type": t_type, "confidence": 0.94, "inventor": "mdsubhanpasha", "formatted": f"{account}|{amount}|{merchant}|{t_type}|en|mdsubhanpasha", "input": txn}

@app.get("/")
def root():
    return {"message": "FinGPT-Omni Running - Patent mdsubhanpasha", "docs": "/docs", "inventor": "mdsubhanpasha"}

@app.post("/parse")
def parse(txn: str = Form(...)):
    return smart_parse(txn)

@app.get("/parse")
def parse_get(txn: str):
    return smart_parse(txn)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

