import teamsService from '../teams.service';
import { mutationTypes } from './teams.mutations';

export const actionTypes = {
    GET_TEAM: 'GET_TEAM',
    GET_TEAMS: 'GET_TEAMS'
};

export const actions = {
    [actionTypes.GET_TEAM]({ commit, state }, payload) {
        if (!state.selectedTeam || state.selectedTeam != payload) {
            teamsService.getTeam(payload).then(response => {
                commit(mutationTypes.SET_SELECTED_TEAM, payload);
                commit(mutationTypes.SET_TEAM_DATA, response.data);
            });
        }
    },
    [actionTypes.GET_TEAMS]({ commit, state }) {
        if (!state.teamsLoaded) {
            teamsService.getTeams().then(response => {
                commit(mutationTypes.SET_TEAMS, response.data.teams);
                commit(mutationTypes.SET_TEAMS_LOADED, true);
            });
        }
    }
};
