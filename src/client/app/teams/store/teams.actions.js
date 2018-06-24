import teamsService from '../teams.service';
import { mutationTypes } from './teams.mutations';

export const actionTypes = {
    GET_TEAMS: 'GET_TEAMS'
};

export const actions = {
    [actionTypes.GET_TEAMS]({ commit, state }) {
        if (!state.teamsLoaded) {
            teamsService.getTeams().then(response => {
                commit(mutationTypes.SET_TEAMS, response.data.teams);
                commit(mutationTypes.SET_TEAMS_LOADED, true);
            });
        }
    }
};
