from flask import Flask, request, render_template, redirect, url_for, abort, send_from_directory, json, jsonify
from flask_cors import CORS, cross_origin

import json

app = Flask(__name__, static_url_path='/static')

CORS(app)


courses = json.load(open('courses.json'))
majors = json.load(open('major.json'))

@app.route('/api/course-list')
def course_list():
    return jsonify([
        {"name":course['name'], 'code':code, 'credits':course['credit_points']}
        for code,course in courses.items()])

@app.route('/api/major-list')
def major_list():
    return jsonify([{
        "name": major['title'],
        "code": major['code'],
        "value": major['code'] + ' - ' + major['title'],
        "label": major['code'] + ' - ' + major['title']
        } for major in majors])

@app.route('/api/course-detail/<course_code>')
def course_details(course_code):
    return jsonify(courses[course_code]);

@app.route('/api/major-detail/<major_code>')
def major_details(major_code):
    return jsonify([
        major
        for major in majors
        if major['code'] == major_code
        ][0])

if __name__ == '__main__':
    app.run(debug=True)
