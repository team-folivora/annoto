import { mount } from "@cypress/vue";
import App from "../../../src/App.vue";

// Label renders correctly and is visible
describe("App", () => {
  it("renders properly", () => {
    mount(App, { props: { username: "" } });
    cy.get("#userLabel").should("be.visible");
  });
});

// Label renders correctly and is visible
describe("App", () => {
  it("shows username", () => {
    mount(App, { props: { username: "" } });
    cy.get("#userLabel").contains("AnnotoUser#1337");
  });
});
