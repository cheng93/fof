import { shallowMount, RouterLinkStub } from '@vue/test-utils';
import toolbar from './toolbar.vue';

describe('Toolbar', () => {
    it('matches snapshot', () => {
        const wrapper = shallowMount(toolbar, {
            propsData: {
                title: 'Hello World'
            },
            stubs: {
                RouterLink: RouterLinkStub
            }
        });
        expect(wrapper.html()).toMatchSnapshot();
    });
});
