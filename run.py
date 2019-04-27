from flask import Flask, request, render_template, redirect, url_for, abort, send_from_directory, json, jsonify
from flask_cors import CORS, cross_origin

import json

app = Flask(__name__, static_url_path='/static')

CORS(app)


courses = json.load(open('courses.json'))

@app.route('/api/course-list')
def course_list():
    return jsonify([{"name":course['name'], 'code':code} for code,course in courses.items()])

@app.route('/api/course-detail/<course_code>')
def course_details(course_code):
    return jsonify(courses[course_code]);


if __name__ == '__main__':
    app.run(debug=True)
