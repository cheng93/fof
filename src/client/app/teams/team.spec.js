import { createLocalVue, mount } from '@vue/test-utils';
import Vuex from 'vuex';
import { actionTypes } from './store/teams.actions';
import team from './team.vue';

describe('Team', () => {
    let wrapper;

    beforeEach(() => {
        const localVue = createLocalVue();
        localVue.use(Vuex);
        const actions = {
            [actionTypes.GET_TEAM]: jest.fn()
        };

        const store = new Vuex.Store({
            modules: {
                teams: {
                    namespaced: true,
                    actions
                }
            }
        });

        const teamData = {
            team_id: 1,
            name: 'Foo',
            wins: 11,
            loses: 10,
            ties: 1,
            win_lose_percent: 0.1111,
            playoff_appearances: 3,
            conference_wins: 2,
            superbowl_wins: 1,
            division: 'Bar'
        };

        const $route = {
            params: {
                id: 1
            }
        };

        wrapper = mount(team, {
            stubs: {
                TeamTable: '<div>Team Table</div>'
            },
            computed: {
                team: () => teamData
            },
            filters: {
                to_percentage: val => `toPercentage(${val})`
            },
            mocks: {
                $route
            },
            store,
            localVue
        });
    });

    it('matches snapshot', () => {
        expect(wrapper.html()).toMatchSnapshot();
    });
});
