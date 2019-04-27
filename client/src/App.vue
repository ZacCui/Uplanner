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

    <!-- course detail modal --> 
    <modal name="course_details"
      height="auto"
      :scrollable="true"
      @closed="modal_course = false">

      <h4 v-if="!modal_course">Loading...</h4>
      <div v-if="modal_course" id="modal_content">
        <h5>{{modal_course.code}} - {{modal_course.name}}</h5>
        <q-chip v-for="keyword in comma_split(modal_course.keywords)"
          color="primary">
          {{keyword}}
        </q-chip>
        <p>
          <a v-if="modal_course.url" :href="modal_course.url">see details in handbook</a>
          <a v-if="!modal_course.url">No Handbook entry for this course</a>
        </p>
        <p>Credits: {{modal_course.credit_points}}</p>
        <p>Contact hours: {{modal_course.contact_hours}}</p>
        <p v-if="modal_course.teaching_period_display">
        Available in: {{modal_course.teaching_period_display}}
        </p>

        <p>{{modal_course.enrol_conditions ? modal_course.enrol_conditions : ""}}</p>
        <div v-html="modal_course.description">
        </div>
      </div>
    </modal>

    <!-- Left Side Drawer -->
    <q-layout-drawer side="left" v-model="showLeft">    
      <!-- major search input -->
      <q-input color="amber" placeholder="Type 'fre'">
        <q-autocomplete
          @search="search_major"
          @selected="major_selected"
          :min-characters="3"
          :value-field="major => `${major.code} - ${major.name}`"
        />
      </q-input>

      <!-- course serach input -->
      <q-input v-model="searchCourse" float-label="Search Course" 
        placeholder="Enter course name or course code" />

      <draggable v-model="courses" group="courses">
        <transition-group>
          <q-item
            v-for="course in courses"
            :key = "course.code"
            highlight
            separator
            link
            @click.native="modal_show(course.code)"
          >
            <small>{{stripString(courseString(course), 40)}}</small>
            <q-tooltip anchor="bottom middle" self="top middle">
              {{courseString(course)}}
            </q-tooltip>
          </q-item>
        </transition-group>
      </draggable>
    </q-layout-drawer>

    <!-- sub-routes get injected here: -->
    <q-page-container>
      <q-list>
        <q-collapsible label="Year 1" opened>
          <div style="display: flex; justify-content: center;">
            <q-card style="width: 300px; margin-right: 20px;">
            <q-card-title>
              Semester 1
            </q-card-title>
            <q-card-separator />
            <q-card-main>
              <draggable v-model="semester1Courses" group="courses">
                <div v-if="semester1Courses.length === 0">
                  <p>Drag a course here</p>
                </div>
                <div v-else>
                  <q-item
                    v-for="course in semester1Courses"
                    :key = "course.code"
                    highlight
                    separator
                    link
                    @click.native="modal_show(course.code)"
                  >
                    <small>{{stripString(courseString(course), 35)}}</small>
                    <q-tooltip anchor="bottom middle" self="top middle">
                      {{courseString(course)}}
                    </q-tooltip>
                  </q-item>
                </div>           
              </draggable>
            </q-card-main>
          </q-card>

          <q-card style="width: 300px; margin-right: 20px;">
            <q-card-title>
              Semester 2
            </q-card-title>
            <q-card-separator />
            <q-card-main>
              Card Content
            </q-card-main>
          </q-card>

          <q-card style="width: 300px;">
            <q-card-title>
              Semester 3
            </q-card-title>
            <q-card-separator />
            <q-card-main>
              Card Content
            </q-card-main>
          </q-card>
          </div>        
        </q-collapsible>

        <q-collapsible label="Year 2" opened>

        </q-collapsible>

        <q-collapsible label="Year 3" opened>

        </q-collapsible>
      </q-list>  
    </q-page-container>
  </q-layout>
</template>

<script>
var API_BASE = 'http://localhost:5000'
import draggable from 'vuedraggable'
import axios from 'axios';

export default {
  name: 'LayoutDefault',
  components: {
    draggable
  },
  data () {
    return {
      modal_course: false,
      selected_courses: [],
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
      semester1Courses: [
        
      ],  
    }
  },
  methods: {
    modal_show (code) {
      this.modal_course = code;
      this.$modal.show('course_details');
      axios.get(API_BASE + '/api/course-detail/' + code)
        .then(res => {
          this.modal_course = res.data;
        })
    },
    courseString: function (course) {
      return `${course.code} - ${course.name}`
    },
    stripString: function (str, limit) {
      if (str.length <= limit) {
        return str
      }

      return str.substr(0, limit) + "..."
    },
    comma_split(str) {
      if(!str)
        return [];
      return str.split(',');
    },
    search_major(terms, done) {
      done(this.all_majors.filter(major => {
        return major.name.toLowerCase().includes(terms.toLowerCase()) ||
          major.code.toLowerCase().includes(terms.toLowerCase());
      }));
    },
    major_selected(item) {
      // this.selected_major = item.code;
      axios
        .get(API_BASE + '/api/major-detail/' + item.code)
        .then(response => {
          this.major_core_courses = response.data.core_courses;
        });
      }
  },
  computed: {
    courses: function() {
      var cores = this.all_courses
        .filter(course => this.major_core_courses.includes(course.code));
      /* match code/name and limit to 20 */
      var matching = this.all_courses.filter(course => {
        if(!this.searchCourse)
          return false;
        return course.code.toLowerCase().includes(this.searchCourse.toLowerCase()) ||
          course.name.toLowerCase().includes(this.searchCourse.toLowerCase());
      }).slice(0, 20);
      return cores.concat(matching).filter(course => {
        return !this.semester1Courses.includes(course);
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
