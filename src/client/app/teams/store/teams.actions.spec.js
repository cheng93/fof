import { actions, actionTypes } from './teams.actions';
import { mutationTypes } from './teams.mutations';
import teamsService from '../teams.service';
jest.mock('../teams.service');

describe('Teams Store: Actions', () => {
    describe(actionTypes.GET_TEAMS, () => {
        it('should fetch from api', async () => {
            const teams = [
                { team_id: 1, team_name: 'Foo' },
                { team_id: 2, team_name: 'Bar' }
            ];

            teamsService.getTeams.mockImplementation(
                () => new Promise(resolve => resolve({ data: { teams } }))
            );
            const commit = jest.fn();
            const state = {};

            const { [actionTypes.GET_TEAMS]: action, ...x } = actions;

            await action({ commit, state });

            expect(commit.mock.calls).toEqual([
                [mutationTypes.SET_TEAMS, teams],
                [mutationTypes.SET_TEAMS_LOADED, true]
            ]);
        });

        it('shouldnt fetch from api when retrieved before', async () => {
            const commit = jest.fn();
            const state = { teamsLoaded: true };

            const { [actionTypes.GET_TEAMS]: action, ...x } = actions;

            await action({ commit, state });

            expect(commit.mock.calls.length).toBe(0);
        });
    });
});
