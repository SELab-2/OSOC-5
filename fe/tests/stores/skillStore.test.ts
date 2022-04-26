import {beforeEach, describe, expect, it, test} from 'vitest'
import {createPinia, setActivePinia} from 'pinia'
import {useSkillStore} from "../../src/stores/useSkillStore";


describe('Skill Store', () => {
    beforeEach(() => {
        // creates a fresh pinia and make it active so it's automatically picked
        // up by any useStore() call without having to pass it to it:
        // `useStore(pinia)`
        setActivePinia(createPinia())
    })

    it('loadSkills', () => {

        // create a new skillstore
        const skillStore = useSkillStore()

        // check its initial values
        expect(skillStore.skills).toHaveLength(0)
        expect(skillStore.isLoadingSkills).toBe(false)



        // test.concurrent('concurrent test 1', async () => {
            // load skills
            skillStore.loadSkills()
            // check if it's loading skills
            expect(skillStore.isLoadingSkills).toBe(true)
        // })


    });
    it('addSkill', () => {

        // create a new skillstore
        const skillStore = useSkillStore()

        // check its initial values
        expect(skillStore.skills).toHaveLength(0)
        expect(skillStore.isLoadingSkills).toBe(false)

        let callback_finished = false

        test.concurrent('add skill and wait', async () => {
            // load skills
            skillStore.addSkill("newSkillName", "color", () => { callback_finished = true})

            expect(callback_finished).toBeTruthy()
        })


    });
    it('deleteSkill', () => {

        // create a new skillstore
        const skillStore = useSkillStore()

        // check its initial values
        expect(skillStore.skills).toHaveLength(0)
        expect(skillStore.isLoadingSkills).toBe(false)

        // load skills
        skillStore.deleteSkill(-1)

    })
})