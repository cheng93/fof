export const mutationTypes = {
    SET_TEAMS: 'SET_TEAMS',
    SET_TEAMS_LOADED: 'SET_TEAMS_LOADED'
};

export const mutations = {
    [mutationTypes.SET_TEAMS](state, teams) {
        state.teams = teams;
    },
    [mutationTypes.SET_TEAMS_LOADED](state, loaded) {
        state.teamsLoaded = loaded;
    }
};
