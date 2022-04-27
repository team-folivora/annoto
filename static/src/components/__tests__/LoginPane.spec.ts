import { mount } from "@cypress/vue";
import UserInformationLabel from "@/components/UserInformationLabel.vue";
import LoginPane from "../LoginView.vue";

describe("LoginPane", () => {
  it("exists", () => {
    mount(LoginPane);
  });

  it("has a field for username", () => {
    mount(LoginPane);
    cy.get("input[name='username']");
  });

  it("has a field for password", () => {
    mount(LoginPane);
    cy.get("input[name='password']");
  });

  it("has a submit button", () => {
    mount(LoginPane);
    cy.get("button#submit");
  });
});
