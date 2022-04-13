// https://docs.cypress.io/api/introduction/api.html

function intercept_get_task() {
  cy.intercept(
    "GET",
    "http://localhost:5000/tasks/ecg-qrs-classification-physiodb",
    { fixture: "task.json" }
  ).as("get_task");
}

function intercept_next_image() {
  cy.intercept(
    "GET",
    "http://localhost:5000/tasks/ecg-qrs-classification-physiodb/next",
    {
      fixture: "nextImage.txt",
    }
  ).as("get_next_image");
}

function intercept_next_image_with_failure() {
  cy.intercept(
    "GET",
    "http://localhost:5000/tasks/ecg-qrs-classification-physiodb/next",
    { statusCode: 404 }
  ).as("get_next_image");
}

describe("Application", () => {
  it("visits the app root url", () => {
    cy.visit("/");
    cy.contains("h1", "Annoto");
  });

  it("shows username", () => {
    cy.visit("/");
    cy.get("#userLabel").contains("AnnotoUser#1337");
  });

  it("informs the user when no more images are available for annotation", () => {
    intercept_get_task();
    intercept_next_image_with_failure();

    cy.visit("/");
    cy.wait("@get_task").then(() => {
      cy.wait("@get_next_image").then(() => {
        cy.get("#no-more-images").should("be.visible");
      });
    });
  });

  it("shows annotation buttons", () => {
    intercept_get_task();
    intercept_next_image();

    cy.visit("/");
    cy.wait("@get_task").then(() => {
      cy.wait("@get_next_image").then(() => {
        cy.screenshot();
        cy.get("#annotation-button-atrial-fibrillation").should("be.visible");
        cy.get("#annotation-button-other").should("be.visible");
      });
    });
  });

  it("shows image display", () => {
    intercept_get_task();
    intercept_next_image();

    cy.visit("/");
    cy.wait("@get_task").then(() => {
      cy.wait("@get_next_image").then(() => {
        cy.get("#image-display").should("be.visible");
      });
    });
  });
});
