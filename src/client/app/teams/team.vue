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
        <v-data-table
            :headers="headers"
            :items="team.seasons"
            hide-actions
            class="elevation-1">
             <template slot="items" slot-scope="props">
                <td>
                    {{props.item.year}}
                </td>
                <td>{{ props.item.wins }}</td>
                <td>{{ props.item.loses }}</td>
                <td>{{ props.item.ties }}</td>
                <td>{{ props.item.win_lose_percent | to_percentage }}</td>
                <td>{{ props.item.standing_name }}</td>
                </template>
        </v-data-table>
    </section>
</template>
<script>
import { mapState } from 'vuex';
import { actionTypes } from './store/teams.actions';

export default {
    computed: mapState({
        team: state => state.teams.teamData
    }),
    created() {
        this.$store.dispatch(
            `teams/${actionTypes.GET_TEAM}`,
            this.$route.params.id
        );
    },
    data() {
        return {
            headers: [
                {
                    text: 'Season',
                    value: 'year'
                },
                {
                    text: 'Wins',
                    value: 'wins'
                },
                {
                    text: 'Loses',
                    value: 'loses'
                },
                {
                    text: 'Ties',
                    value: 'ties'
                },
                {
                    text: 'WL%',
                    value: 'win_lose_percent'
                },
                {
                    text: 'Standing',
                    value: 'standing_name'
                }
            ]
        };
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

