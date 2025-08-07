from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
import csv
import io

from main import scrape_courses, export_to_csv

app = Flask(__name__)
CORS(app)

@app.route('/api/scrape', methods=['POST'])
def scrape_endpoint():
    data = request.json
    query = data.get('courseName', '')
    degree_types = data.get('degreeTypes', ['bachelor', 'master'])
    languages = data.get('languages', ['english'])
    start_periods = data.get('startPeriods', ['winter'])
    limit = data.get('universityLimit', 10)
    course_data = scrape_courses(query, degree_types, languages, start_periods, limit)

    return jsonify({
        "success": True,
        "data": course_data,
        "count": len(course_data)
    })

@app.route('/api/export-csv', methods=['POST'])
def export_csv():
    data = request.json
    courses = data.get('data', [])
    
    if not courses:
        return jsonify({"success": False, "error": "No course data provided"})
    csv_content = export_to_csv(courses)
    
    # Create response with CSV file
    response = app.response_class(
        csv_content,
        mimetype='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename=course_results.csv'
        }
    )
    
    return response

if __name__ == '__main__':
    # app.run(debug=True, port=5000)
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)