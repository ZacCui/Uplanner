<template>
  <q-collapsible :label="year.name" opened="true">
    <template slot="header">
      <q-item-main :label="year.name" />
      <q-item-side v-if="index == years - 1" right>
        <q-btn
          round
          icon="close"
          color="negative"
          @click="deleteYear()"
        />
      </q-item-side>
    </template>

    <div style="display: flex; justify-content: center;">
      <Semester
        :highlight="highlightTerms.includes(semester.name)"
        v-for="(semester, index) in year.semesters"
        :key="index"
        :index="index"
        :name="semester.name"
        :group="group"
        :value="semester.courses"
        v-on:input="emitChange"
        :courses="semester.courses"
        style="margin-right: 20px;"
        v-on:hoverCourse="hover"
        v-on:stopHoverCourse="stopHover()"
        :prereqs="prereqs"
        :cores="cores"
        v-on:startDragging="startDragging"
        v-on:stopDragging="stopDragging"
        :loaded_local_storage='loaded_local_storage'
      />
    </div>
  </q-collapsible>
</template>

<script>
import Semester from '@/components/Semester.vue'

export default {
  name: 'Year',
  props: [
    'value',
    'group',
    'opened',
    'prereqs',
    'cores',
    'index',
    'years',
    'highlightTerms',
    'loaded_local_storage'
  ],
  components: {
    Semester
  },
  computed: {
    year() {
      return this.value
    }
  },
  methods: {
    startDragging(evt) {
      this.$emit('startDragging', evt);
    },
    stopDragging() {
      this.$emit('stopDragging');
    },
    deleteYear() {
      this.$emit('deleteYear');
    },
    hover(code) {
      this.$emit('hoverCourse', code);
    },
    stopHover() {
      this.$emit('stopHoverCourse');
    },
    emitChange: function(courses, semesterIndex) {
      this.$emit('input', courses, semesterIndex, this.index);
    }
  }
}
</script>
