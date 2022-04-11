import { mount } from "@cypress/vue";
import UserInformationLabel from "../UserInformationLabel.vue";

// Label exists
describe("UserInformationLabel", () => {
  it("exists", () => {
    mount(UserInformationLabel, { props: { username: "" } });
  });

  it("prints label text correctly", () => {
    const name = "Annoto#1337";
    mount(UserInformationLabel, { props: { username: name } });
    const text = "Current logged in user:";
    cy.get("div").contains(text);
    cy.get("#userLabel").contains(name);
  });
});
