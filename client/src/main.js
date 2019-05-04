import Vue from 'vue'
import Vue2TouchEvents from 'vue2-touch-events'
import App from './App.vue'

import 'quasar-extras/roboto-font'
import 'quasar-extras/material-icons'
import Quasar from 'quasar'
import VModal from 'vue-js-modal'
import {config} from './config'
import './styles/quasar.styl'


Vue.use(Vue2TouchEvents);

Vue.use(Quasar, {
  config: {}
});

Vue.use(VModal);

Vue.config.productionTip = false;

Vue.prototype.$config = config;

new Vue({
  render: h => h(App),
}).$mount('#app');
