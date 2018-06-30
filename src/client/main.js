import Vue from 'vue';
import Vuetify from 'vuetify';
import app from './app/app';
import router from './app/router';
import store from './app/store';
import './app/filters';

Vue.use(Vuetify);

new Vue({
    router,
    store,
    el: '#app',
    render: h => h(app)
});

import './vendor.scss';
