<template>
  <q-collapsible :label="year.name" :opened="opened">
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
        :name="semester.name"
        :group="group"
        v-model="semester.courses"
        style="margin-right: 20px;"
        v-on:hoverCourse="hover"
        v-on:stopHoverCourse="stopHover()"
        :prereqs="prereqs"
        :cores="cores"
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
    'highlightTerms'
  ],
  components: {
    Semester
  },
  data() {
    return {
      year: this.value
    }
  },
  methods: {
    deleteYear() {
      this.$emit('deleteYear');
    },
    hover(code) {
      this.$emit('hoverCourse', code);
    },
    stopHover() {
      this.$emit('stopHoverCourse');
    },
    emitChange: function() {
      this.$emit('input', this.year);
    }
  }
}
</script>
