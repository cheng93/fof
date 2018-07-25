import axios from 'axios';

export default {
    getSeasons(teamId) {
        return axios.get(`api/teams/${teamId}/seasons`);
    },
    getTeam(teamId) {
        return axios.get(`api/teams/${teamId}`);
    },
    getTeams() {
        return axios.get('api/teams');
    }
};
