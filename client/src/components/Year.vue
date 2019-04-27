<template>
  <q-collapsible :label="year.name" :opened="opened">
    <div style="display: flex; justify-content: center;">
      <Semester
        v-for="(semester, index) in year.semesters"
        :key="index"
        :name="semester.name"
        :group="group"
        v-model="semester.courses"
        style="margin-right: 20px;"
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
    'opened'
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
    emitChange: function() {
      this.$emit('input', this.year);
    }
  }
}
</script>
