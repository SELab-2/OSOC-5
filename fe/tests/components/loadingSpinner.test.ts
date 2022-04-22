import {expect, describe, beforeEach, vi, it} from 'vitest'
import {mount} from '@vue/test-utils'
import {Quasar} from 'quasar'
import LoadingSpinner from '../../src/components/LoadingSpinner.vue'
import {createPinia, setActivePinia} from "pinia";
import {createTestingPinia} from '@pinia/testing'

// This makes sure Quasar is loaded
const wrapperFactory = () => mount(LoadingSpinner, {
    global: {
        plugins: [
            createTestingPinia({
                createSpy: vi.fn,
            }),
            Quasar
        ]
    },
})

describe('LoadingSpinner.vue', () => {
    // this makes sure Pinia is loaded before every test
    beforeEach(() => {
        setActivePinia(createPinia())
    })

    it('Test if spinner loads correctly', () => {
        expect(LoadingSpinner).toBeTruthy();
        const wrapper = wrapperFactory();
        expect(wrapper.find('.q-spinner').exists()).toBeTruthy()
    })
})
