export const mutationTypes = {
    SET_SELECTED_TEAM: 'SET_SELECTED_TEAM',
    SET_TEAM_DATA: 'SET_TEAM_DATA',
    SET_TEAMS: 'SET_TEAMS',
    SET_TEAMS_LOADED: 'SET_TEAMS_LOADED'
};

export const mutations = {
    [mutationTypes.SET_SELECTED_TEAM](state, teamId) {
        state.selectedTeam = teamId;
    },
    [mutationTypes.SET_TEAM_DATA](state, teamData) {
        state.teamData = teamData;
    },
    [mutationTypes.SET_TEAMS](state, teams) {
        state.teams = teams;
    },
    [mutationTypes.SET_TEAMS_LOADED](state, loaded) {
        state.teamsLoaded = loaded;
    }
};
