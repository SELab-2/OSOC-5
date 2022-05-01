import { beforeEach, describe, expect, it, test } from "vitest";
import { createPinia, setActivePinia } from "pinia";
import { useCoachStore } from "../../src/stores/useCoachStore";

const baseURL = "https://sel2-5.ugent.be/api/";

describe("Skill Store", () => {
  beforeEach(() => {
    // creates a fresh pinia and make it active so it's automatically picked
    // up by any useStore() call without having to pass it to it:
    // `useStore(pinia)`
    setActivePinia(createPinia());
  });

  it("getUser", () => {

    const coachStore = useCoachStore();

    expect(coachStore.isLoadingUsers).toBe(false);

    coachStore.getUser(baseURL + "coaches/-1")

  });

  it("loadUsers", () => {

    const coachStore = useCoachStore();

    expect(coachStore.isLoadingUsers).toBe(false);

    coachStore.loadUsers()
    expect(coachStore.isLoadingUsers).toBe(true);

  });
});