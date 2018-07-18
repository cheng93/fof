<template>
    <v-data-table
        :headers="headers"
        :items="seasons"
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
</template>
<script>
import { mapState } from 'vuex';
import { actionTypes } from './store/teams.actions';

export default {
    computed: mapState({
        seasons: state => state.teams.teamData.seasons
    }),
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

