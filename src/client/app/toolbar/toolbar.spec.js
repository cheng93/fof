import { mount, RouterLinkStub } from '@vue/test-utils';
import toolbar from './toolbar.vue';

describe('Toolbar', () => {
    let wrapper;

    beforeEach(() => {
        wrapper = mount(toolbar, {
            propsData: {
                title: 'Hello World'
            },
            stubs: {
                RouterLink: RouterLinkStub
            }
        });
    });
    it('matches snapshot', () => {
        expect(wrapper.html()).toMatchSnapshot();
    });

    it('should link to home', () => {
        expect(wrapper.find(RouterLinkStub).props().to).toBe('/');
    });
});
