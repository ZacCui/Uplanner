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
      <draggable v-model="courses" group="courses">
        <transition-group>
          <q-item
            v-for="course in courses"
            :key = "course.code"
            highlight
            separator
            link
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
import draggable from 'vuedraggable'

export default {
  name: 'LayoutDefault',
  components: {
    draggable
  },
  data () {
    return {
      showLeft: true,
      searchCourse: "",
      courses: [
        {
          code: "INFO1000",
          name: "Introduction to Programming"
        },
        {
          code: "INFO1001",
          name: "Introduction to Programming 1"
        },
        {
          code: "INFO1002",
          name: "Introduction to Programming 2 What"
        }
      ],
      semester1Courses: [
        
      ],  
    }
  },
  methods: {
    courseString: function (course) {
      return `${course.code} - ${course.name}`
    },
    stripString: function (str, limit) {
      if (str.length <= limit) {
        return str
      }

      return str.substr(0, limit) + "..."
    }
  }
}
</script>

<style lang="stylus">


</style>
