<template>
    <section>
        <h1 class="mdc-typography--headline5">{{team.name}}</h1>
        <dl>
            <dt class="mdc-typography--subtitle2">
                Division:
            </dt>
            <dd class="mdc-typography--body2">
                {{team.division}}
            </dd>
            <dt class="mdc-typography--subtitle2">
                Record (W-L-T):
            </dt>
            <dd class="mdc-typography--body2">
                {{team.wins}}-{{team.loses}}-{{team.ties}}
            </dd>
            <dt class="mdc-typography--subtitle2">
                Win-Lose %:
            </dt>
            <dd class="mdc-typography--body2">
                {{team.win_lose_percent | to_percentage}}
            </dd>
            <dt class="mdc-typography--subtitle2">
                Playoff Appearances:
            </dt>
            <dd class="mdc-typography--body2">
                {{team.playoff_appearances}}
            </dd>
            <dt class="mdc-typography--subtitle2">
                Conference Wins:
            </dt>
            <dd class="mdc-typography--body2">
                {{team.conference_wins}}
            </dd>
            <dt class="mdc-typography--subtitle2">
                Superbowl Wins:
            </dt>
            <dd class="mdc-typography--body2">
                {{team.superbowl_wins}}
            </dd>
        </dl>
        <tabs :headers="headers">
            <template slot="tab-0">
                <team-table></team-table>
            </template>
            <template slot="tab-1">
                Hello World
            </template>
        </tabs>
    </section>
</template>
<script>
import { mapState } from 'vuex';
import { actionTypes } from './store/teams.actions';
import store from '../store';

import tabs from '../components/tabs/tabs';
import teamTable from './team.table';

export default {
    computed: mapState({
        team: state => state.teams.teamData
    }),
    beforeRouteEnter(to, from, next) {
        store
            .dispatch(`teams/${actionTypes.GET_TEAM}`, to.params.id)
            .then(() => next());
    },
    data() {
        return {
            headers: ['Table', 'Chart']
        };
    },
    components: {
        tabs,
        teamTable
    }
};
</script>
<style lang="scss" scoped>
h1,
dl {
    margin: 12px 0;
}
dl {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    max-width: 248px;

    dt {
        flex: 1 1 124px;
    }
}
</style>

