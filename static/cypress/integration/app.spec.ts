import { login, setupIntercepts } from "./utils";

describe("Application", () => {
  it("visits the app root url", () => {
    cy.visit("/").contains("h1", "Annoto");
  });
  
  it("shows no logout button when the user is not logged in", () => {
    cy.visit("/").get("#logout-button").should("not.exist");
  });

  it("shows a logout button when the user is logged in", () => {
    setupIntercepts();
    login().get("#logout-button");
  });

  it("Logout button redirects to login page", () => {
    setupIntercepts();
    login().get("#logout-button").click({ force: true }).get("#login-view");
  });
});
