<template>
    <section>
        <h1 class="mdc-typography--headline5">Teams</h1>
        <v-data-table
            :headers="headers"
            :items="teams"
            hide-actions
            class="elevation-1">
             <template slot="items" slot-scope="props">
                <td>{{ props.item.name }}</td>
                <td>{{ props.item.wins }}</td>
                <td>{{ props.item.loses }}</td>
                <td>{{ props.item.ties }}</td>
                <td>{{ props.item.win_lose_percent | win_lose_percent }}</td>
                <td>{{ props.item.playoff_appearances }}</td>
                <td>{{ props.item.conference_wins }}</td>
                <td>{{ props.item.superbowl_wins }}</td>
                </template>
        </v-data-table>
    </section>
</template>
<script>
import numeral from 'numeral';
import { mapState } from 'vuex';
import { actionTypes } from './teams.store';

export default {
    computed: mapState({
        teams: state => state.teams.teams
    }),
    created() {
        this.$store.dispatch(`teams/${actionTypes.GET_TEAMS}`);
    },
    data() {
        return {
            headers: [
                {
                    text: 'Team',
                    value: 'name'
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
                    text: 'Playoffs',
                    value: 'playoff_appearances'
                },
                {
                    text: 'Conference',
                    value: 'conference_wins'
                },
                {
                    text: 'Superbowl',
                    value: 'superbowl_wins'
                }
            ]
        };
    },
    filters: {
        win_lose_percent: function(value) {
            return `${numeral(value * 100).format('0.00')}%`;
        }
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

