import axios from 'axios';

export default {
    getTeams() {
        return axios.get('api/teams');
    }
};
