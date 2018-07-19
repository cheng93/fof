<script>
import numeral from 'numeral';
import palette from 'google-palette';
import { mapState } from 'vuex';
import { Bar } from 'vue-chartjs';

export default {
    computed: mapState({
        labels: state => state.teams.teamData.seasons.map(s => s.year),
        datasets(state) {
            var colours = palette('tol-rainbow', 3).map(function(hex) {
                return '#' + hex;
            });
            var keys = {
                win_lose_percent: {
                    label: 'WL%',
                    type: 'line',
                    map(s) {
                        return numeral(s.win_lose_percent * 100).format('0.00');
                    },
                    borderColor: colours[0],
                    fill: false,
                    yAxisID: 'B'
                },
                wins: {
                    label: 'Wins',
                    backgroundColor: colours[1],
                    yAxisID: 'A'
                },
                loses: {
                    label: 'loses',
                    backgroundColor: colours[2],
                    yAxisID: 'A'
                }
            };
            return Object.entries(keys).map(([key, option]) => ({
                ...option,
                data: state.teams.teamData.seasons.map(
                    s => (option.map && option.map(s)) || s[key]
                )
            }));
        }
    }),
    extends: Bar,
    mounted() {
        // Overwriting base render method with actual data.
        let data = {
            labels: this.labels,
            datasets: this.datasets
        };
        let options = {
            maintainAspectRatio: false,
            scales: {
                yAxes: [
                    {
                        id: 'A',
                        type: 'linear',
                        position: 'left',
                        gridLines: {
                            display: false
                        }
                    },
                    {
                        id: 'B',
                        type: 'linear',
                        gridLines: {
                            display: false
                        },
                        position: 'right',
                        ticks: {
                            min: 0,
                            max: 100
                        }
                    }
                ]
            }
        };
        this.renderChart(data, options);
    }
};
</script>
