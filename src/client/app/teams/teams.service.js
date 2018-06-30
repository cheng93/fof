import axios from 'axios';

export default {
    getTeam(teamId) {
        return axios.get(`api/teams/${teamId}`);
    },
    getTeams() {
        return axios.get('api/teams');
    }
};
