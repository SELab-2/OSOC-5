import {test, expect, describe, beforeEach, fn, vi} from 'vitest'
import {mount} from '@vue/test-utils'
import {Quasar} from 'quasar'
import Component from '../../src/components/LoadingSpinner.vue'
import {createPinia, setActivePinia} from "pinia";
import {createTestingPinia} from '@pinia/testing'

// This makes sure Quasar is loaded
const wrapperFactory = () => mount(Component, {
    global: {
        plugins: [
            createTestingPinia({
                createSpy: vi.fn,
            }),
            Quasar
        ]
    },
})

describe('example test typescript', () => {
    // this makes sure Pinia is loaded before every test
    beforeEach(() => {
        setActivePinia(createPinia())
    })
    // example test
    test('mount component', () => {
        expect(Component).toBeTruthy();
        const wrapper = wrapperFactory();

        // console.log(wrapper.html());
    })
})
