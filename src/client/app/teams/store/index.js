import { actions } from './teams.actions';
import { getters } from './teams.getters';
import { mutations } from './teams.mutations';
import { state } from './teams.state';

export default {
    namespaced: true,
    actions,
    getters,
    mutations,
    state
};
