<template>
  <q-card style="width: 400px; min-height: 100px;">
    <q-card-title>
      {{name}}
    </q-card-title>
    <q-card-separator />
    <q-card-main>
      <draggable
        v-model="courses"
        :group="group"
        @input="emitChange"
        style="min-height: 100px;"
      >
        <CourseItem 
          v-for="course in courses"
          :key="course.code"
          :course="course"
          :isRemoveable="true"
          :onRemove="onRemoveCourse"
        />
      </draggable>
    </q-card-main>
  </q-card>
</template>

<script>
import draggable from 'vuedraggable'
import CourseItem from '@/components/CourseItem.vue'

export default {
  name: 'Semester',
  props: [
    'value',
    'name',    
    'group'
  ],
  components: {
    draggable,
    CourseItem
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
    }
  }
}
</script>