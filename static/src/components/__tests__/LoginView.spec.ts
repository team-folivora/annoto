import { mount } from "@cypress/vue";
import LoginView from "../LoginView.vue";

describe("LoginView", () => {
  it("exists", () => {
    mount(LoginView);
  });

  it("has a field for email", () => {
    mount(LoginView);
    cy.get("i-input[name='email']");
  });

  it("has a field for password", () => {
    mount(LoginView);
    cy.get("i-input[name='password']");
  });

  it("has a submit button", () => {
    mount(LoginView);
    cy.get("i-button#submit");
  });
});
