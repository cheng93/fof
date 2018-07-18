<template>
    <div>
        <nav class="mdc-tab-bar">
            <span v-for="(header, index) in headers"
                :key="index"
                v-on:click="selectIndex(index)"
                v-bind:class="{'mdc-tab--active': selectedIndex == index}"
                class="mdc-tab">
                {{header}}
            </span>
        </nav>
        <div v-for="(header, index) in headers"
            :key="index"
            v-if="selectedIndex == index">
            <slot :name="'tab-' + index"></slot>
        </div>
    </div>
</template>
<script>
export default {
    data() {
        return {
            selectedIndex: 0
        };
    },
    methods: {
        selectIndex: function(index) {
            this.selectedIndex = index;
        }
    },
    props: {
        headers: {
            type: Array,
            required: true
        }
    }
};
</script>
