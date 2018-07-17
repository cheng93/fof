import { actions, actionTypes } from './teams.actions';
import { mutationTypes } from './teams.mutations';
import teamsService from '../teams.service';
jest.mock('../teams.service');

describe('Teams Store: Actions', () => {
    describe(actionTypes.GET_TEAM, () => {
        describe('when it needs to fetch from api', () => {
            let team;
            beforeEach(() => {
                team = { team_id: 1, team_name: 'Foo' };
                teamsService.getTeam.mockImplementation(
                    payload => new Promise(resolve => resolve({ data: team }))
                );
            });

            it('should fetch from api when no team is selected', async () => {
                const commit = jest.fn();
                const state = { selectedTeam: null };
                const teamId = team.team_id;

                const { [actionTypes.GET_TEAM]: action, ...x } = actions;

                await action({ commit, state }, teamId);

                expect(commit.mock.calls).toEqual([
                    [mutationTypes.SET_SELECTED_TEAM, teamId],
                    [mutationTypes.SET_TEAM_DATA, team]
                ]);
            });

            it('should fetch from api when different team is selected', async () => {
                const commit = jest.fn();
                const state = { selectedTeam: 2 };
                const teamId = team.team_id;

                const { [actionTypes.GET_TEAM]: action, ...x } = actions;

                await action({ commit, state }, teamId);

                expect(commit.mock.calls).toEqual([
                    [mutationTypes.SET_SELECTED_TEAM, teamId],
                    [mutationTypes.SET_TEAM_DATA, team]
                ]);
            });
        });

        it('should not fetch from api when team is already selected', async () => {
            const commit = jest.fn();
            const selectedTeam = 1;
            const state = { selectedTeam };

            const { [actionTypes.GET_TEAM]: action, ...x } = actions;

            await action({ commit, state }, selectedTeam);

            expect(commit.mock.calls.length).toBe(0);
        });
    });

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
