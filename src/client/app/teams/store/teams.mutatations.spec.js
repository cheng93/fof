import { mutations, mutationTypes } from './teams.mutations';

describe('Teams Store: Mutations', () => {
    it(mutationTypes.SET_SELECTED_TEAM, () => {
        const state = { selectedTeam: null };
        const teamId = 1;

        const { [mutationTypes.SET_SELECTED_TEAM]: mutation, ...x } = mutations;

        mutation(state, teamId);

        expect(state.selectedTeam).toEqual(teamId);
    });

    it(mutationTypes.SET_TEAM_DATA, () => {
        const state = { teamData: {} };
        const team = { team_id: 1, team_name: 'Foo' };

        const { [mutationTypes.SET_TEAM_DATA]: mutation, ...x } = mutations;

        mutation(state, team);

        expect(state.teamData).toEqual(team);
    });

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
