import {expect, describe, it} from 'vitest'
import {mount} from '@vue/test-utils'
import LoadingSpinner from '../../src/components/LoadingSpinner.vue'

const wrapperFactory = () => mount(LoadingSpinner, {})

describe('LoadingSpinner.vue', () => {

    it('Test if spinner loads correctly', () => {
        expect(LoadingSpinner).toBeTruthy();
        const wrapper = wrapperFactory();
        expect(wrapper.find('.q-spinner').exists()).toBeTruthy()
    })
})
