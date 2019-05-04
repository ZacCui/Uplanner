<template>
  <q-card :color="highlight ? 'light' : ''" class="term-card">
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
        @start="startDragging($event)"
        @end="stopDragging()"
      >
        <CourseItem 
          v-for="course in courses"
          :key="course.code"
          :course="course"
          :isRemoveable="true"
          :onRemove="onRemoveCourse"
          v-on:hoverCourse="hover"
          v-on:stopHoverCourse="stopHover()"
          :prereqs="prereqs"
          :cores="cores"
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
    'group',
    'prereqs',
    'cores',
    'highlight',
    'index',
    'loaded_local_storage'
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
    hover(code) {
      this.$emit('hoverCourse', code);
    },
    stopHover() {
      this.$emit('stopHoverCourse');
    },
    startDragging(evt) {
      this.$emit('startDragging', evt);
    },
    stopDragging() {
      this.$emit('stopDragging');
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
    onRemoveCourse: function (removedCourse) {
      // filter in place
      // filterInPlace(this.courses, course => removedCourse.code !== course.code)
      this.courses = this.courses.filter(course => removedCourse.code !== course.code);
      this.emitChange();
    },
    emitChange: function () {
      this.$emit('input', this.courses, this.index)
    }
  },
  watch: {
    loaded_local_storage: {
      handler() {
        this.courses = this.value;
      }
    }
  
  }
}
</script>
