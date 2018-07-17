<template>
    <div id="app">
        <toolbar :title=title />
        <div class="mdc-top-app-bar--fixed-adjust">
            <div class="page">
                <router-view></router-view>
            </div>
        </div>
    </div>
</template>

<script>
import toolbar from './toolbar/toolbar';

export default {
    name: 'app',
    components: {
        toolbar
    },
    computed: {
        title() {
            return 'Front Office Football';
        }
    }
};
</script>
<style>
body {
    margin: 0;
}

a {
    text-decoration: inherit;
    color: inherit;
}

h1,
ul {
    margin: 0px;
}

ul {
    list-style-type: none;
    padding: 0px;
}
</style>
<style scoped>
.page {
    margin: 24px 36px;
}
</style>




