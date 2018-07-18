import { createLocalVue, mount, RouterLinkStub } from '@vue/test-utils';
import Vuex from 'vuex';
import Vuetify from 'vuetify';
import { actionTypes } from './store/teams.actions';
import teamTable from './team.table.vue';

describe('Team Table', () => {
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

        const seasons = [
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
        ];

        const $route = {
            params: {
                id: 1
            }
        };

        wrapper = mount(teamTable, {
            stubs: {
                RouterLink: RouterLinkStub
            },
            computed: {
                seasons: () => seasons
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
