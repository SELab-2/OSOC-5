import {expect, describe, it} from 'vitest'
import {mount} from '@vue/test-utils'
import NotFoundPage from '../../src/components/NotFoundPage.vue'

const wrapperFactory = () => mount(NotFoundPage, {})

describe('NotFoundPage.vue', () => {

    it('Test if the text is displayed correctly', () => {
        expect(NotFoundPage).toBeTruthy();
        const wrapper = wrapperFactory();
        expect(wrapper.find('h1').exists()).toBeTruthy()
        expect(wrapper.find('h1').text()).toEqual("404: Page not found.")
    })
})