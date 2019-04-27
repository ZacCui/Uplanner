<template>
  <q-item    
    highlight
    separator
    link
    @click.native="loadCourseDetails(); showModal = !showModal"
    @mouseover.native="hover()"
    @mouseleave.native="stopHover()"
  >
		<q-chip dense v-if="cores.includes(course.code)" color="primary">
			Core
		</q-chip>

		<q-chip dense v-if="prereqs.includes(course.code)" color="secondary">
      Prereq
		</q-chip>
    <q-item-main>
      <small>{{stripString(courseString(course), lengthLimit)}}</small>
      <q-tooltip anchor="bottom middle" self="top middle">
        {{courseString(course)}}
        <br>
        {{details.enrol_conditions}}
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
          <p class="q-title">Study Level</p>
          <p>{{details.study_level}}</p>
          
          <p class="q-title">Contact Hours</p>      
          <p>{{details.contact_hours}}</p>

          <p class="q-title">Credit Points</p>
          <p>{{details.credit_points}}</p>

          <p class="q-title">Teaching Period</p>
          <p v-html="details.teaching_period_display"></p>

          <p v-if="details.enrol_conditions" class="q-title">Enrol Conditions</p>
          <p v-html="details.enrol_conditions"></p>

          <p class="q-title">Description</p>
          <p v-html="details.description"></p>

          <p class="q-title">Offical Handbook</p>
          <a v-if="details.url" target="_blank" :href="details.url">{{details.url}}</a>
          <a v-if="!details.url">No handbook entry</a>


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
    },
    prereqs: {
      type: Array,
      default: () => []
    },
    cores: {
      type: Array,
      default: () => []
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
    hover: function (){
      this.loadCourseDetails();
      this.$emit('hoverCourse', this.course.code);
    },
    stopHover() {
      this.$emit('stopHoverCourse');
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
    loadCourseDetails: function () {
      if (this.isLoaded) {
        return
      }

      axios
        .get(`http://localhost:5000/api/course-detail/${this.course.code}`)
        .then(res => {
          this.details = res.data
          // eslint-disable-next-line
          this.isLoaded = true
        })
    }
  }
}
</script>

<style lang="stylus">

  .q-chip
    margin-right 5px

</style>
