from helper_functions import split_and_execute_queries
from flask import Flask, jsonify
from db_conn import get_mysql_conn


data = split_and_execute_queries(get_mysql_conn(), 'sql_query.sql')

app = Flask(__name__)


@app.route("/get-waec-records/<school_exam_id>/<exam_year>")
def get_waec_records(school_exam_id, exam_year):

    # Filter the DataFrame
    filtered_data = data[
        (data["school_exam_id"] == int(school_exam_id)) & 
        (data["exam_year"] == int(exam_year))
    ]

    status = "success" if not filtered_data.empty else "failure"
    results_count = len(filtered_data)

    waec_records_data = {
        "status": status,
        "records": results_count,
        "data": filtered_data.to_dict(orient="records") 
    }

    return jsonify(waec_records_data), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)