from fastapi import FastAPI
from employee_offboarding import router

app = FastAPI(title="Employee Offboarding Security Test")
app.include_router(router)
