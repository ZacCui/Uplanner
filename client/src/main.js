import Vue from 'vue'
import App from './App.vue'

import './styles/quasar.styl'
import 'quasar-extras/roboto-font'
import 'quasar-extras/material-icons'
import Quasar from 'quasar'
import VModal from 'vue-js-modal'


Vue.use(Quasar, {
  config: {}
 })

Vue.use(VModal)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
