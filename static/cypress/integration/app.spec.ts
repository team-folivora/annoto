import { login, setupIntercepts } from "./utils";
import { task } from "../fixtures/fixture_objects";

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

  it("logout button redirects to login page", () => {
    setupIntercepts();
    login().get("#logout-button").click({ force: true }).get("#login-view");
  });

  it("redirects to login if trying to access tasks and not logged in", () => {
    setupIntercepts();
    cy.visit("/tasks").url().should("include", "/login");
  });

  it(`redirects to login if trying to access tasks/${task.id} and not logged in`, () => {
    setupIntercepts();
    cy.visit(`/tasks/${task.id}`).url().should("include", "/login");
  });

  it(`redirects to login if trying to access / and not logged in`, () => {
    setupIntercepts();
    cy.visit("/").url().should("include", "/login");
  });

  it("redirects to tasks if trying to access /login and logged in", () => {
    setupIntercepts();
    login().visit("/login").url().should("include", "/tasks");
  });

  it(`redirects to tasks if trying to access / and logged in`, () => {
    setupIntercepts();
    login().visit("/").url().should("include", "/tasks");
  });
});
