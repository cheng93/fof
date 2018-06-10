import Vue from 'vue';
import app from './app/app';
import router from './app/router';
import store from './app/store';

new Vue({
    router,
    store,
    el: '#app',
    render: h => h(app)
});
