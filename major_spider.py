import scrapy
import json

class MajorSpider(scrapy.Spider):
    payload = '{"track_scores":true,"_source":{"includes":["*.code","*.name","*.award_titles","*.keywords","urlmap","contenttype"],"excludes":["",null,null]},"query":{"filtered":{"query":{"bool":{"must":[{"query_string":{"fields":["*study_level_value*"],"query":"*ugrd*"}},{"bool":{"minimum_should_match":"100%","should":[{"query_string":{"fields":["*implementation_year*"],"query":"*2019*"}}]}}]}},"filter":{"bool":{"should":[{"term":{"contenttype":"aos"}}],"must_not":[{"missing":{"field":"*.name"}},{"term":{"subject.published_in_handbook":"0000000000000000000.000000000000000000"}}]}}}},"from":0,"size":500,"sort":[{"aos.code":"asc"}]} '
    name = 'major'
    urls = []
    base_url = "https://www.handbook.unsw.edu.au"

    def start_requests(self):
        return [scrapy.Request("https://www.handbook.unsw.edu.au/api/es/search",
                method='POST', body=self.payload, 
                headers={'Content-Type': 'application/json',
                'Accept': '*/*', 'Connection': 'keep-alive'},
                callback=self.got_list)]

    def got_list(self, res):
        data = json.loads(res.text);
        for entry in data['contentlets']:
            if 'URL_MAP_FOR_CONTENT' not in entry:
                continue
            url = self.base_url + entry['URL_MAP_FOR_CONTENT']
            yield res.follow(url, self.parse)


    def parse(self, response):
        title = response.css('div#subject-intro span[data-hbui="module-title"]::text').get()
        code = response.css('div#subject-intro > div > div > h3.no-margin > strong::text').get()
        core_courses = response.css('div[data-hbui-filter-group="related-courses"] div.m-single-course-wrapper div.m-single-course-top-row span.align-left::text').getall()
        yield {
            'code': code,
            'title': title,
            'core_courses': core_courses
        }
