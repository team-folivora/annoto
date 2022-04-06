import { mount } from "@cypress/vue";
import UserInformationLabel from "../UserInformationLabel.vue";
import App from "../../App.vue";

// Label exists
describe("UserInformationLabel", () => {
  it("exists", () => {
    mount(UserInformationLabel, { props: { username: "" } });
  });
});

// Label renders correctly and is visible
describe("App", () => {
  it("renders properly", () => {
    mount(App, { probs: { username: "" } });
    cy.get("#userLabel").should("be.visible");
  });
});

// Label renders correctly and is visible
describe("App", () => {
  it("shows username", () => {
    mount(App, { probs: { username: "" } });
    cy.get("#userLabel").contains("AnnotoUser#1337");
  });
});
