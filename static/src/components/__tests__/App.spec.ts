import { mount } from "@cypress/vue";
import App from "../../../src/App.vue";

describe("App", () => {
  it("exists", () => {
    mount(App);
  });

  it("shows annotation buttons", () => {
    mount(App);
    cy.get("#annotation-button-Faultier").should("be.visible");
    cy.get("#annotation-button-Maus").should("be.visible");
  });

  it("shows image display", () => {
    mount(App);
    cy.get("#image-display").should("be.visible");
  });

  it("renders properly", () => {
    mount(App);
    cy.get("#userLabel").should("be.visible");
  });

  it("shows username", () => {
    mount(App);
    cy.get("#userLabel").contains("AnnotoUser#1337");
  });
});
