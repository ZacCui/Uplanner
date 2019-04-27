<template>
  <q-item    
    highlight
    separator
    link
    @click.native="loadCourseDetails(); showModal = !showModal"
  >
    <q-item-main>
      <small>{{stripString(courseString(course), lengthLimit)}}</small>
      <q-tooltip anchor="bottom middle" self="top middle">
        {{courseString(course)}}
      </q-tooltip>
    </q-item-main>
    <q-item-side right v-if="isRemoveable">
      <q-btn dense round flat icon="close" @click="onRemove(course)" />
    </q-item-side>

    <q-modal v-model="showModal" :content-css="{maxWidth: '80vw', minHeight: '80vh'}">
      <q-modal-layout>
        <q-toolbar slot="header">
          <q-toolbar-title>
            {{courseString(course)}}
          </q-toolbar-title>
        </q-toolbar>

        <div class="layout-padding">
          <p class="q-title">Code</p>
          <p>{{details.code}}</p>
          
          <p class="q-title">Name</p>
          <p>{{details.name}}</p>
          
          <p class="q-title">Study Level</p>
          <p>{{details.study_level}}</p>
          
          <p class="q-title">Description</p>
          <div v-html="details.description"></div>

          <p class="q-title">Contact Hours</p>      
          <p>{{details.contact_hours}}</p>

          <p class="q-title">Credit Points</p>
          <p>{{details.credit_points}}</p>

          <p class="q-title">Teaching Period</p>
          <div v-html="details.teaching_period_display"></div>
        </div>        
      </q-modal-layout>
    </q-modal>
  </q-item>  
</template>

<script>
import axios from 'axios'

export default {
  name: 'CourseItem',
  props: {
    course: {
      type: Object,
      required: true
    },
    lengthLimit: {
      type: Number,
      default: 35
    },
    isRemoveable: {
      type: Boolean,
      default: false
    },
    onRemove: {
      type: Function,
      default: function () { }
    }
  },
  data () {
    return {
      showModal: false,
      details: {},
      isLoaded: false      
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
    },
    loadCourseDetails: function () {
      if (this.isLoaded) {
        return
      }

      axios
        .get(`http://localhost:5000/api/course-detail/${this.course.code}`)
        .then(res => {
          this.details = res.data
          // eslint-disable-next-line
          console.log(res.data)
          this.isLoaded = true
        })
    }
  }
}
</script>