<template>
  <q-card style="width: 400px;">
    <q-card-title>
      {{name}}
    </q-card-title>
    <q-card-separator />
    <q-card-main>
      <draggable
        v-model="courses"
        :group="group"
        @input="emitChange"
        :move="onMove"
      >
        <p v-if="false">Drag a course here</p>
        <q-item
          v-else
          v-for="course in courses"
          :key = "course.code"
          highlight
          separator
          link       
        >
          <q-item-main>
            <small>{{stripString(courseString(course), 35)}}</small>
            <q-tooltip anchor="bottom middle" self="top middle">
              {{courseString(course)}}
            </q-tooltip>
          </q-item-main>
          <q-item-side right>
            <q-btn dense round flat icon="close" @click="onRemoveCourse(course)" />
          </q-item-side>
        </q-item>
      </draggable>
    </q-card-main>
  </q-card>
</template>

<script>
import draggable from 'vuedraggable'

export default {
  name: 'Semester',
  props: [
    'value',
    'name',    
    'group'
  ],
  components: {
    draggable
  },
  data() {
    return {
      courses: this.value
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
    onRemoveCourse: function (removedCourse) {
      this.courses = this.courses.filter(course => removedCourse.code !== course.code);
      this.emitChange();
    },
    emitChange: function () {
      this.$emit('input', this.courses)
    },
    /* eslint-disable */
    onMove: function (event) {
      console.log(event.from)
      console.log(event.to)
    }
  }
}
</script>