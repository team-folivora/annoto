import { mount } from "@cypress/vue";
import LoginView from "../LoginView.vue";

describe("LoginView", () => {
  it("exists", () => {
    mount(LoginView);
  });

  it("has a field for username", () => {
    mount(LoginView);
    cy.get("input[name='username']");
  });

  it("has a field for password", () => {
    mount(LoginView);
    cy.get("input[name='password']");
  });

  it("has a submit button", () => {
    mount(LoginView);
    cy.get("button#submit");
  });
});
