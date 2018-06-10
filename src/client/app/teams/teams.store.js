import teamsService from './teams.service';

export const actionTypes = {
    GET_TEAMS: 'GET_TEAMS'
};

export const mutationTypes = {
    SET_TEAMS: 'SET_TEAMS'
};

const state = {
    teams: []
};

const getters = {};

const actions = {
    [actionTypes.GET_TEAMS]({ commit }) {
        teamsService
            .getTeams()
            .then(response =>
                commit(mutationTypes.SET_TEAMS, response.data.teams)
            );
    }
};

const mutations = {
    [mutationTypes.SET_TEAMS](state, teams) {
        state.teams = teams;
    }
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
};
