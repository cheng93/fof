import teamsService from '../teams.service';
import { mutationTypes } from './teams.mutations';

export const actionTypes = {
    GET_TEAM: 'GET_TEAM',
    GET_TEAMS: 'GET_TEAMS'
};

export const actions = {
    [actionTypes.GET_TEAM]({ commit, state }, payload) {
        if (!state.selectedTeam || state.selectedTeam != payload) {
            return Promise.all([
                teamsService.getTeam(payload),
                teamsService.getSeasons(payload)
            ]).then(([team, seasons]) => {
                commit(mutationTypes.SET_SELECTED_TEAM, payload);
                const teamData = {
                    ...team.data,
                    ...seasons.data
                };
                commit(mutationTypes.SET_TEAM_DATA, teamData);
            });
        }
    },
    [actionTypes.GET_TEAMS]({ commit, state }) {
        if (!state.teamsLoaded) {
            return teamsService.getTeams().then(response => {
                commit(mutationTypes.SET_TEAMS, response.data.teams);
                commit(mutationTypes.SET_TEAMS_LOADED, true);
            });
        }
    }
};
