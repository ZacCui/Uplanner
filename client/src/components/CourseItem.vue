<template>
  <q-item    
    highlight
    separator
    link
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
  </q-item>
</template>

<script>
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
  }
}
</script>