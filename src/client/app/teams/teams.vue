<template>
    <section>
        <h1 class="mdc-typography--headline5">Teams</h1>
        <ul>
            <li v-for="team in teams" :key="team.team_id">
                <router-link :to="'teams/' + team.team_id">{{team.city}} {{team.team_name}}</router-link>
            </li>
        </ul>
    </section>
</template>
<script>
import { mapState } from 'vuex';
import { actionTypes } from './teams.store';

export default {
    computed: mapState({
        teams: state => state.teams.teams
    }),
    created() {
        this.$store.dispatch(`teams/${actionTypes.GET_TEAMS}`);
    }
};
</script>

<style scoped>
h1 {
    margin: 12px 0;
}

ul {
    display: flex;
    flex-wrap: wrap;
}

li {
    flex: 0 1 200px;
    margin: 12px 0;
}
</style>

