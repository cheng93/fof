import Vue from 'vue';
import VueRouter from 'vue-router';

import homeRoutes from './home/home.routes';
import teamsRoutes from './teams/teams.routes';

Vue.use(VueRouter);

const routes = [...homeRoutes, ...teamsRoutes];

export default new VueRouter({
    routes: routes,
    scrollBehavior(to, from, savedPosition) {
        return savedPosition ? savedPosition : { x: 0.0, y: 0.0 };
    }
});
