import { createLocalVue, mount, RouterLinkStub } from '@vue/test-utils';
import Vuex from 'vuex';
import Vuetify from 'vuetify';
import { actionTypes } from './store/teams.actions';
import team from './team.vue';

describe('Team', () => {
    let wrapper;

    beforeEach(() => {
        const localVue = createLocalVue();
        localVue.use(Vuex);
        localVue.use(Vuetify);
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
            division: 'Bar',
            seasons: [
                {
                    year: 2015,
                    wins: 2,
                    loses: 1,
                    ties: 1,
                    win_lose_percent: 0.3333,
                    standing_name: 'Regular'
                },
                {
                    year: 2016,
                    wins: 3,
                    loses: 0,
                    ties: 0,
                    win_lose_percent: 1,
                    standing_name: 'Runner Up'
                }
            ]
        };

        const $route = {
            params: {
                id: 1
            }
        };

        wrapper = mount(team, {
            stubs: {
                RouterLink: RouterLinkStub
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
