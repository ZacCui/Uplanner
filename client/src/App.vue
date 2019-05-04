<template>
  <q-layout view="hHr LpR lFf" v-touch:moving="movingHandler">
    <q-layout-header>
      <q-toolbar>
        <q-btn
          flat round dense
          @click="showLeft = !showLeft"
          icon="menu"
        />
        <q-toolbar-title>
          Uplanner - Uni Course Planner
        </q-toolbar-title>
        <img src="favicon.ico" />
      </q-toolbar>
    </q-layout-header>

    <!-- Left Side Drawer -->
    <q-layout-drawer side="left" v-model="showLeft">    

      <!-- major search input -->
      <q-select
        style="padding-left: 5px"
        filter
        v-model="major_search_string"
        :display-value="stripString(major_search_string, 30)"
        :options="all_majors"
        @input="search_major"
        placeholder="Enter your major here"
      />

      <!-- course serach input -->
      <q-input 
        style="padding-left: 5px"
        v-model="searchCourse" float-label="Search Course" 
        placeholder="Enter course name or course code" />
      <draggable
        id="course-list" 
        v-model="courses"
        :group="{
          name: 'courses',
          pull: 'clone',
          put: false
        }"
        :move="onMoveCallback"
        @start="startDragging($event)"
        @end="stopDragging()"
      >
        <transition-group>
          <CourseItem 
            v-for="course in courses"
            :key="course.code"
            :course="course"
            :lengthLimit="40"
            :prereqs="prereqs"
            :cores="major_core_courses"
          />
        </transition-group>
      </draggable>
    </q-layout-drawer>

    <!-- right panel -->
    <q-page-container>
      <q-toolbar width=window.width color="deep-purple-7">
          <q-toolbar-title>
            Enrolled credits: <b>{{total_credits}}</b>
          </q-toolbar-title>
          <q-btn @click="clear()" 
            color="negative" 
            class="float-right" 
            label="Clear"
            style="margin-right: 5px"/>
          <q-btn @click="save()" 
            color='deep-purple-10' 
            class="float-right" 
            label="Save results" />
    </q-toolbar>
      <q-list>
        <Year
          v-for="(_year, index) in years"
          :key="index"
          :index="index"
          :years="years.length"
          :value="_year"
          group="courses"
          v-on:hoverCourse="hover"
          v-on:stopHoverCourse="stop_hover"
          :cores="major_core_courses"
          :prereqs="prereqs"
          v-on:deleteYear="deleteYear"
          :highlightTerms="dragging_course_periods"
          v-on:startDragging="startDragging"
          v-on:stopDragging="stopDragging"
          :loaded_local_storage="loaded_local_storage"
          v-on:input="updateCourses"
        />
      </q-list>  
      <q-btn
        class="add-btn"
        round
        icon="add"
        color="primary"
        @click="add_year"
      >
      </q-btn>
    </q-page-container>
  </q-layout>
</template>

<script>
import draggable from 'vuedraggable'
import axios from 'axios'
import Year from '@/components/Year.vue'
import CourseItem from '@/components/CourseItem.vue'
import { scroll } from 'quasar'
const { getScrollTarget, setScrollPosition } = scroll


export default {
  name: 'LayoutDefault',
  components: {
    Year,
    CourseItem,
    draggable
  },
  data () {
    return {
      fingerIcon: document.createElement("div"),
      loaded_local_storage: false,
      selected_courses: [],
      major_search_string: "",
      major_core_courses: [],
      hover_course: "",
      dragging_course_periods: [],
      prereqs: [],
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
              name: 'Summer Term',
              courses: []              
            },
            {
              name: 'Term 1',
              courses: []              
            },
            {
              name: 'Term 2',
              courses: []              
            },
            {
              name: 'Term 3',
              courses: []              
            },
          ]
        },
        {
          name: 'Year 2',
          semesters: [
            {
              name: 'Summer Term',
              courses: []              
            },
            {
              name: 'Term 1',
              courses: []              
            },
            {
              name: 'Term 2',
              courses: []              
            },
            {
              name: 'Term 3',
              courses: []              
            },
          ]
        },
        {
          name: 'Year 3',
          semesters: [
            {
              name: 'Summer Term',
              courses: []              
            },
            {
              name: 'Term 1',
              courses: []              
            },
            {
              name: 'Term 2',
              courses: []              
            },
            {
              name: 'Term 3',
              courses: []              
            },
          ]
        }
      ]
    }
  },
  methods: {
    movingHandler(event) {
      const fingerX = event.changedTouches[0].pageX;
      const fingerY = event.changedTouches[0].pageY;
      this.fingerIcon.style.setProperty("top", fingerY + "px");
      this.fingerIcon.style.setProperty("left", fingerX + "px");
    },
    clear() {
      if(confirm("Are you sure to clear the existing plan"))
        this.years = [];
    },
    stripString: function (str, limit) {
      if (str.length <= limit) {
        return str
      }
      return str.substr(0, limit) + "..."
    },
    add_year() {
      this.years.push({
        name: 'Year ' + (this.years.length + 1),
        semesters: [
          {
            name: 'Summer Term',
            courses: []              
          },
          {
            name: 'Term 1',
            courses: []              
          },
          {
            name: 'Term 2',
            courses: []              
          },
          {
            name: 'Term 3',
            courses: []              
          }
        ]
      });
    },
    deleteYear() {
      this.years = this.years.slice(0, this.years.length - 1);
    },
    startDragging(evt) {
      let code = evt.item.querySelector('small').innerText.split(' - ')[0];
      axios.get(`${this.$config.API_BASE}/course-detail/${code}`)
        .then(res => {
          if(res.data.teaching_period_display)
            this.dragging_course_periods = 
              res.data.teaching_period_display.split(', ')
        });
      if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
        // We are going to check if we are running a mobile system. If mobile,
        // hide the left drawer when dragging.
        this.showLeft = false;
        // Since draggable is not implemented on mobile, we have to fake it on
        // the system.
        if (!this.fingerIconOn) {
          this.fingerIconOn = true;
          this.fingerIcon.textContent = "sdfoidspsdf";
          document.body.appendChild(this.fingerIcon);
        }
      }
    },
    stopDragging() {
      this.dragging_course_periods = [];
      // Hide the finger Icon we have dragged
      if (this.fingerIconOn) {
        this.fingerIconOn = false;
        this.fingerIcon.hidden = true;
      }
    },
    hover(code) {
      let vue = this;
      vue.hover_course = code;
      setTimeout(() => {
        if(vue.hover_course != code)
          return;
        axios
          .get(`${this.$config.API_BASE}/course-detail/${code}`)
          .then(res => {
            let re = /[A-Z]{4}[0-9]{4}/g;
            if(res.data.enrol_conditions) {
              let target = getScrollTarget(document.getElementById('course-list'));
              this.prereqs = res.data.enrol_conditions.match(re)
              setScrollPosition(target, 0, 500)
            }
            if(!res.data.enrol_conditions || !this.prereqs)
              this.prereqs = [];
          })
      }, 500);
    },
    stop_hover() {
      this.hover_course = "";
    },
    search_major(terms) {
      this.major_search_string = terms;
      let code = terms.split(' - ')[0];
      axios.get(this.$config.API_BASE + '/major-detail/' + code)
        .then(res => {
          this.major_core_courses = res.data.core_courses;
        })
        .catch(() => {
          this.major_core_courses = [];
        })
    },
    // eslint-disable-next-line
    onMoveCallback: function(event) {
      if(event.from === event.to){
        return false
      }        
      return true
    },
    save() {
      const parsed = JSON.stringify(this.years);
      localStorage.setItem('years', parsed);
      localStorage.setItem('major', this.major_search_string);
      alert('Plan saved');
    },
    updateCourses(courses, semesterIndex, yearIndex) {
      this.years[yearIndex].semesters[semesterIndex].courses = courses;
    }


  },
  computed: {
    total_credits() {
      let result = 0;
      for (const year of this.years) {
        for (const semester of year.semesters) {
          for (const c of semester.courses) {
            if(c.credits)
              result += parseInt(c.credits)
          }
        }
      }
      return result;
    },
    courses: function() {
      let matched = this.all_courses.filter(course => {
        if(!this.searchCourse)
          return false;
        return course.code.toLowerCase().includes(this.searchCourse.toLowerCase()) ||
          course.name.toLowerCase().includes(this.searchCourse.toLowerCase());
      }).slice(0, 10);

      let cores = []
      if(this.major_core_courses)
        cores = this.all_courses
          .filter(course => this.major_core_courses.includes(course.code))
          .map(course => {course.core = true; return course});

      let prereq = this.all_courses
        .filter(course => this.prereqs.includes(course.code))
        .map(course => {course.prereq = true; return course});

      let result = matched.concat(prereq).concat(cores);

      let codes = [];

      return result.filter(course => {
        if(codes.includes(course.code))
          return false;
        codes.push(course.code);
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
        return !selected;
      });
    }
  },
  mounted () {
    axios
      .get(this.$config.API_BASE + '/course-list')
      .then(response => {this.all_courses = response.data;});
    axios
      .get(this.$config.API_BASE + '/major-list')
      .then(response => {
        this.all_majors = [{label: 'Choose your major', value: ''}].concat(response.data);
      });
    if (localStorage.getItem('years')) {
      if(localStorage.getItem('major'))
        this.search_major(localStorage.getItem('major'));
      try {
        this.years = JSON.parse(localStorage.getItem('years'));
        this.loaded_local_storage = true;
      } catch(e) {
        localStorage.removeItem('years');
      }
    }
    this.fingerIcon = document.createElement("div");
    this.fingerIcon.setAttribute("class", "hover-item");
  },
}
</script>

<style lang="stylus">
  div#modal_content {
    padding: 10px 5px;
  }

  .add-btn {
    margin: 10px 20px;
  }

  img {
    width: 30px;
    height: 30px;
  }

</style>
