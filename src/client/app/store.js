import Vue from 'vue';
import Vuex from 'vuex';

import teams from './teams/store';

Vue.use(Vuex);

const modules = {
    teams
};

export default new Vuex.Store({
    modules: modules
});
