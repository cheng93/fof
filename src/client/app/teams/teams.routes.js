import team from './team';
import teams from './teams';

const routes = [
    { path: '/teams', component: teams },
    { path: '/teams/:id', component: team }
];

export default routes;
