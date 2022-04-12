// https://docs.cypress.io/api/introduction/api.html

describe("Application", () => {
  beforeEach(() => {
    cy.intercept(
      "GET",
      "http://localhost:5000/tasks/ecg-qrs-classification-physiodb",
      { fixture: "task.json" }
    ).as("get_task");
    cy.visit("/");
  });

  it("visits the app root url", () => {
    cy.contains("h1", "Annoto");
  });

  it("shows username", () => {
    cy.get("#userLabel").contains("AnnotoUser#1337");
  });

  it("shows annotation buttons", () => {
    cy.wait("@get_task").then(() => {
      cy.get("#annotation-button-atrial-fibrillation").should("be.visible");
      cy.get("#annotation-button-other").should("be.visible");
    });
  });

  it("shows image display", () => {
    cy.wait("@get_task").then(() => {
      cy.get("#image-display").should("be.visible");
    });
  });
});
