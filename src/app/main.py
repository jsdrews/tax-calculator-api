from fastapi import FastAPI

from app.routes.tax_calculator.routes import router as tax_calculator_router

app = FastAPI()
app.include_router(tax_calculator_router)


@app.get("/")
def root():
    return {"hello": "world"}
