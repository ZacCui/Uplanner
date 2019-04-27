import requests
import json
import re
import os
import time
from tqdm import tqdm
from queue import Queue
from threading import Thread

domain = 'https://www.handbook.unsw.edu.au'
base_url = 'https://www.handbook.unsw.edu.au/Undergraduate/courses/2019/'
prereq_re = re.compile(r'<div>(Prerequisite: .*)<\/div>')
COURSE_KEYS = ['URL_MAP_FOR_CONTENT', 'code', 'contact_hours', 'credit_points',
               'description', 'keywords', 'name', 'study_level', 'teaching_period_display']
NUM_THREADS = 5


def prereq_runner(courses, processed_courses, pbar):
    while not courses.empty():
        course = courses.get()
        try:
            if os.path.isfile('webpages/{}.html'.format(course['code'])):
                raise Exception('{} already scraped'.format(course['code']))
            url = base_url + course['code'] + '/'
            r = requests.get(url)
            if r.status_code != 200:
                print("ERROR {} {}".format(r.status_code, url))
            else:
                prereq = prereq_re.findall(r.text)
                # store all course webpages
                with open("webpages/{}.html".format(course['code']), 'w') as f:
                    f.write(r.text)

                if len(prereq) > 0:
                    course = {**dict(course), 'enrol_conditions': prereq[0]}
                    # print(prereq[0])
            processed_courses.append(course)
            time.sleep(0.5)
        except Exception as e:
            print(e)
        finally:
            pbar.update()
            courses.task_done()

def parse_local():
    data = json.load(open('data.json'))
    courses = {course['code']: {key: course[key] for key in COURSE_KEYS if key in course}
            for course in data['contentlets']
            if course['content_type_label'] == 'Course' and
            course['study_level'] == 'Undergraduate'}
    processed_courses = {}
    for code, course in courses.items():
        if 'URL_MAP_FOR_CONTENT' in course:
            course['url'] = domain + course['URL_MAP_FOR_CONTENT']
        try:
            with open('webpages/{}.html'.format(course['code'])) as html:
                prereq = prereq_re.findall(html.read())
                if len(prereq) > 0:
                    course = {**dict(course), 'enrol_conditions': prereq[0]}
                processed_courses[course['code']] = course
        except Exception as e:
            processed_courses[course['code']] = course
    json.dump(processed_courses, open('processed_courses.json', 'w'))

def parse():
    if not os.path.exists('webpages'):
        os.makedirs('webpages')
    data = json.load(open('data.json'))
    courses = {course['code']: {key: course[key] for key in COURSE_KEYS if key in course}
            for course in data['contentlets']
            if course['content_type_label'] == 'Course' and
            course['study_level'] == 'Undergraduate'}

    programs = [course for course in data['contentlets']
            if course['content_type_label'] == 'Program']

    specialisations = [course for course in data['contentlets']
            if course['content_type_label'] == 'Specialisation']

    courses_q = Queue()
    for course in courses.values():
        courses_q.put(course)

    pbar = tqdm(total=len(courses))
    processed_courses = []
    print('Scraping course prerequisites...')
    for _ in range(NUM_THREADS):
        t = Thread(target=prereq_runner, args=(courses_q, processed_courses, pbar))
        t.setDaemon(True)
        t.start()

    courses_q.join()

    courses = {course['code']: course for course in processed_courses}

    json.dump(courses, open('courses.json', 'w'))
    print('Courses with prereq stored in courses.json')


def scrape():
    payload = json.loads('{"track_scores":true,"_source":{"includes":["*.code","*.name","*.award_titles","*.keywords","*.active","urlmap","contenttype"],"excludes":["",null,null]},"query":{"filtered":{"query":{"bool":{"must":[]}},"filter":{"bool":{"should":[{"term":{"contenttype":"subject"}},{"term":{"contenttype":"course"}},{"term":{"contenttype":"aos"}}],"must_not":[{"missing":{"field":"*.name"}}]}}}},"from":0,"size":6500,"sort":[{"subject.code":"asc","aos.code":"asc","course.code":"asc"}]}')

    r = requests.post('https://www.handbook.unsw.edu.au/api/es/search', json=payload)

    data = json.loads(r.text)

    json.dump(data, open('data.json', 'w'))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Options for scraper')
    parser.add_argument('option', choices=['scrape', 'parse', 'local'])
    args = parser.parse_args()

    if args.option == 'scrape':
        scrape()
    elif args.option == 'parse':
        parse()
    elif args.option == 'local':
        parse_local()
