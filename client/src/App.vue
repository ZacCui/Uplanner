<template>
  <q-layout view="hHr LpR lFf">
    <q-layout-header>
      <q-toolbar>
        <q-btn
          flat round dense
          @click="showLeft = !showLeft"
          icon="menu"
        />
        <q-toolbar-title>
          Course Planner
        </q-toolbar-title>
      </q-toolbar>
    </q-layout-header>

    <!-- Left Side Drawer -->
    <q-layout-drawer side="left" v-model="showLeft">    

      <!-- major search input -->
      <q-select
        filter
        v-model="major_search_string"
        :options="all_majors"
        @input="search_major"
        placeholder="Enter your major here"
      />

      <!-- course serach input -->
      <q-input v-model="searchCourse" float-label="Search Course" 
        placeholder="Enter course name or course code" />
      <draggable
        v-model="courses"
        :group="{
          name: 'courses',
          pull: 'clone',
          put: false
        }"
        :move="onMoveCallback"
      >
        <transition-group>
          <CourseItem 
            v-for="course in courses"
            :key="course.code"
            :course="course"
            :lengthLimit="40"
          />
        </transition-group>
      </draggable>
    </q-layout-drawer>

    <q-page-container>
      <q-list>
        <Year
          v-for="(year, index) in years"
          :key="index"
          v-model="years[index]"
          :opened="index === 0"
          group="courses"
        />
      </q-list>  
    </q-page-container>
  </q-layout>
</template>

<script>
var API_BASE = 'http://localhost:5000'
import draggable from 'vuedraggable'
import axios from 'axios'
import Year from '@/components/Year.vue'
import CourseItem from '@/components/CourseItem.vue'

export default {
  name: 'LayoutDefault',
  components: {
    Year,
    CourseItem,
    draggable
  },
  data () {
    return {
      selected_courses: [],
      major_search_string: "",
      major_core_courses: [],
      showLeft: true,
      searchCourse: "",
      all_majors: [],
      all_courses: [
        {
          code: "Loading",
          name: ""
        }
      ],
      years: [
        {
          name: 'Year 1',
          semesters: [
            {
              name: 'Semester 1',
              courses: []              
            },
            {
              name: 'Semester 2',
              courses: []              
            },
            {
              name: 'Semester 3',
              courses: []              
            },
          ]
        },
        {
          name: 'Year 2',
          semesters: [
            {
              name: 'Semester 1',
              courses: []              
            },
            {
              name: 'Semester 2',
              courses: []              
            },
            {
              name: 'Semester 3',
              courses: []              
            },
          ]
        },
        {
          name: 'Year 3',
          semesters: [
            {
              name: 'Semester 1',
              courses: []              
            },
            {
              name: 'Semester 2',
              courses: []              
            },
            {
              name: 'Semester 3',
              courses: []              
            },
          ]
        }
      ]
    }
  },
  methods: {
    search_major(terms) {
      this.major_search_string = terms;
      let code = terms.split(' - ')[0];
      axios.get(API_BASE + '/api/major-detail/' + code)
        .then(res => {
          this.major_core_courses = res.data.core_courses;
        })
    },
    /*
    major_selected(code) {
      // this.selected_major = item.code;
      axios
        .get(API_BASE + '/api/major-detail/' + code)
        .then(response => {
          this.major_core_courses = response.data.core_courses;
        });
    },
    */
    // eslint-disable-next-line
    onMoveCallback: function(event) {
      if(event.from === event.to){
        return false
      }        
      return true
    }
  },
  computed: {
    courses: function() {
      let cores = []
      if(this.major_core_courses)
        cores = this.all_courses
          .filter(course => this.major_core_courses.includes(course.code));

      let matched = this.all_courses.filter(course => {
        if(!this.searchCourse)
          return false;
        if(cores.includes(course))
          return false;
        return course.code.toLowerCase().includes(this.searchCourse.toLowerCase()) ||
          course.name.toLowerCase().includes(this.searchCourse.toLowerCase());
      }).slice(0, 10);

      let result = cores.concat(matched);

      return result.filter(course => {
        let selected = false;
        for (const year of this.years) {
          for (const semester of year.semesters) {
            for (const c of semester.courses) {
              if (c.code === course.code) {
                selected = true;
                break;
              }
            }
            if (selected) {
              break;
            }
          }
          if (selected) {
            break;
          }
        }
        
        return matched && !selected;
      });
    }
  },
  mounted () {
    axios
      .get(API_BASE + '/api/course-list')
      .then(response => {this.all_courses = response.data;});
    axios
      .get(API_BASE + '/api/major-list')
      .then(response => {this.all_majors = response.data;});
  }

}
</script>

<style lang="stylus">
  div#modal_content {
    padding: 10px 5px;
  }

</style>
