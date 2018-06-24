import { mutations, mutationTypes } from './teams.mutations';

describe('Teams Store: Mutations', () => {
    it(mutationTypes.SET_TEAMS, () => {
        const state = { teams: [] };
        const teams = [
            { team_id: 1, team_name: 'Foo' },
            { team_id: 2, team_name: 'Bar' }
        ];

        const { [mutationTypes.SET_TEAMS]: mutation, ...x } = mutations;

        mutation(state, teams);

        expect(state.teams).toEqual(teams);
    });

    it(mutationTypes.SET_TEAMS_LOADED, () => {
        const state = { teams: [] };

        const { [mutationTypes.SET_TEAMS_LOADED]: mutation, ...x } = mutations;

        mutation(state, true);

        expect(state.teamsLoaded).toBe(true);
    });
});
