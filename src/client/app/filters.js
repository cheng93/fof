import numeral from 'numeral';
import Vue from 'vue';

Vue.filter('to_percentage', value => `${numeral(value * 100).format('0.00')}%`);
