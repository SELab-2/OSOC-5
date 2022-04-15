import {it, expect, describe, beforeEach} from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import {useSkillStore} from "../../src/stores/useSkillStore";


describe('Skill Store', () => {
    beforeEach(() => {
        // creates a fresh pinia and make it active so it's automatically picked
        // up by any useStore() call without having to pass it to it:
        // `useStore(pinia)`
        setActivePinia(createPinia())
    })

    it('load skills', () => {

        // create a new skillstore
        const skillStore = useSkillStore()

        // check its initial values
        expect(skillStore.skills).toHaveLength(0)
        expect(skillStore.isLoadingSkills).toBe(false)

        // load skills
        skillStore.loadSkills()

        // check if it's loading skills
        expect(skillStore.isLoadingSkills).toBe(true)

    })
})