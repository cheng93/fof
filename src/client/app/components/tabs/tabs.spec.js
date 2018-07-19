import { mount } from '@vue/test-utils';
import tabs from './tabs.vue';

describe('Tabs', () => {
    let wrapper;

    beforeEach(() => {
        wrapper = mount(tabs, {
            propsData: {
                headers: ['A', 'B']
            },
            slots: {
                'tab-0': '<div>This is tab A</div>',
                'tab-1': '<div>This is tab B</div>'
            }
        });
    });

    it('matches snapshot', () => {
        expect(wrapper.html()).toMatchSnapshot();
    });

    it('when clicked, should switch tab', () => {
        var otherTab = wrapper.find('.mdc-tab:nth-child(2)');
        otherTab.trigger('click');
        expect(wrapper.vm.selectedIndex).toBe(1);
    });

    it('when on other tab, should match snapshot', () => {
        wrapper.vm.selectedIndex = 1;
        expect(wrapper.html()).toMatchSnapshot();
    });
});
