import { mount, createLocalVue, RouterLinkStub } from '@vue/test-utils';
import Vuex from 'vuex';
import Vuetify from 'vuetify';
import { actionTypes } from './store/teams.actions';
import teams from './teams.vue';

let localVue;

describe('Teams', () => {
    let wrapper;

    beforeEach(() => {
        const localVue = createLocalVue();
        localVue.use(Vuex);
        localVue.use(Vuetify);
        const actions = {
            [actionTypes.GET_TEAMS]: jest.fn()
        };

        const store = new Vuex.Store({
            modules: {
                teams: {
                    namespaced: true,
                    actions
                }
            }
        });

        const teamsData = [
            {
                team_id: 1,
                name: 'Foo',
                wins: 11,
                loses: 10,
                ties: 1,
                win_lose_percent: 11.11,
                playoff_appearances: 5,
                conference_wins: 3,
                superbowl_wins: 2
            },
            {
                team_id: 2,
                name: 'Bar',
                wins: 6,
                loses: 5,
                ties: 0,
                win_lose_percent: 50,
                playoff_appearances: 0,
                conference_wins: 0,
                superbowl_wins: 0
            }
        ];

        wrapper = mount(teams, {
            stubs: {
                RouterLink: RouterLinkStub
            },
            computed: {
                teams: () => teamsData
            },
            store,
            localVue
        });
    });

    it('matches snapshot', () => {
        expect(wrapper.html()).toMatchSnapshot();
    });

    it('should have correct router links', () => {
        var links = wrapper.findAll(RouterLinkStub);

        expect(links.at(0).props().to).toBe('/teams/2');
        expect(links.at(1).props().to).toBe('/teams/1');
    });
});
