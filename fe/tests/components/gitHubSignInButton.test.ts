import {expect, describe, it} from 'vitest'
import {mount} from '@vue/test-utils'
import gitHubSignInButton from '../../src/features/authentication/components/gitHubSignInButton.vue'

const wrapperFactory = () => mount(gitHubSignInButton, {})

describe('gitHubSignInButton.vue', () => {

    // it('Test if the gitHub Button is displayed correctly', () => {
    //     expect(gitHubSignInButton).toBeTruthy();
    //     const wrapper = wrapperFactory();
    //     expect(wrapper.find('.q-btn').exists())
    // })
})