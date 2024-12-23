from fastapi import FastAPI, HTTPException
from db_conn import get_mysql_conn
from helper_functions import split_and_execute_queries
import pandas as pd

# Load the data using the helper function
waec_grades_data = split_and_execute_queries(get_mysql_conn(), 'waec_sql_query.sql')
sat_scores_data = split_and_execute_queries(get_mysql_conn(), 'sat_sql_query.sql')

app = FastAPI()

@app.get("/get-waec-records")
def get_waec_records(
    school_exam_id: int, 
    exam_year: int, 
    skip: int = 0, 
    limit: int = 10
):
    # Filter the DataFrame
    filtered_data = waec_grades_data[
        (waec_grades_data["school_exam_id"] == school_exam_id) & 
        (waec_grades_data["exam_year"] == exam_year)
    ]
    
    if filtered_data.empty:
        raise HTTPException(status_code=404, detail="No records found")

    waec_records_data = {
        "status": "success",
        "records": len(filtered_data),
        "data": filtered_data.to_dict(orient="records") 
    }

    return waec_records_data



@app.get("/get-sat-scores")
def get_sat_records(
    ceeb_code: int, 
    exam_year: int, 
    skip: int = 0, 
    limit: int = 10
):
    # Filter the DataFrame
    filtered_data = sat_scores_data[
        (sat_scores_data["ceeb_code"] == ceeb_code) & 
        (sat_scores_data["exam_year"] == exam_year)
    ]
    
    if filtered_data.empty:
        raise HTTPException(status_code=404, detail="No records found")

    sat_records_data = {
        "status": "success",
        "records": len(filtered_data),
        "data": filtered_data.to_dict(orient="records") 
    }

    return sat_records_data