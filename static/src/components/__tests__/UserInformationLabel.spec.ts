import { mount } from "@cypress/vue";
import UserInformationLabel from "../UserInformationLabel.vue";

// Label exists
describe("UserInformationLabel", () => {
  it("exists", () => {
    mount(UserInformationLabel, { props: { username: "" } });
  });
});

describe("UserInformationLabel", () => {
  it("label text printed correctly", () => {
    mount(UserInformationLabel, { props: { username: "" } });
    const text = "Current logged in user:";
    cy.get('[data-v-app=""] > div').contains(text);
  });
});
