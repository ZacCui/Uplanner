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

    <modal name="course_details" @close="showModal = false">
      <h3 slot="header">test</h3>
    </modal>

    <q-layout-drawer side="left" v-model="showLeft">
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
          <q-item
            v-for="course in courses"
            :key = "course.code"
            highlight
            separator
            link
            @click.native="show"
          >
            <small>{{stripString(courseString(course), 40)}}</small>
            <q-tooltip anchor="bottom middle" self="top middle">
              {{courseString(course)}}
            </q-tooltip>
          </q-item>
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
import draggable from 'vuedraggable'
import axios from 'axios'
import Year from '@/components/Year.vue'

export default {
  name: 'LayoutDefault',
  components: {
    Year,
    draggable
  },
  data () {
    return {
      showModal: false,
      selected_courses: [],
      showLeft: true,
      searchCourse: "",
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
    show () {
      this.$modal.show('course_details');
    },
    hide () {
      this.$modal.hide('course_details');
    },
    // eslint-disable-next-line
    onMoveCallback: function(event) {
      if(event.from === event.to){
        return false
      }        
      return true
    },
    courseString: function (course) {
      return `${course.code} - ${course.name}`
    },
    stripString: function (str, limit) {
      if (str.length <= limit) {
        return str
      }

      return str.substr(0, limit) + "..."
    }
  },
  computed: {
    courses: function() {
      return this.all_courses.filter(course => {
        let matched = course.code.toLowerCase().includes(this.searchCourse.toLowerCase()) ||
          course.name.toLowerCase().includes(this.searchCourse.toLowerCase());

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
      }).slice(0, 10);
    }
  },
  mounted () {
    axios
      .get('http://localhost:5000/api/course-list')
      .then(response => {this.all_courses = response.data;})
  }

}
</script>

<style lang="stylus">


</style>
