// https://docs.cypress.io/api/introduction/api.html

function intercept_get_task() {
  cy.intercept(
    "GET",
    `${Cypress.env("API_URL")}/tasks/ecg-qrs-classification-physiodb`,
    { fixture: "task.json" }
  ).as("get_task");
}

function intercept_next_image() {
  cy.intercept(
    "GET",
    `${Cypress.env("API_URL")}/tasks/ecg-qrs-classification-physiodb/next`,
    {
      fixture: "nextImage.txt",
    }
  ).as("get_next_image");
}

function intercept_next_image_with_failure() {
  cy.intercept(
    "GET",
    `${Cypress.env("API_URL")}/tasks/ecg-qrs-classification-physiodb/next`,
    { statusCode: 404 }
  ).as("get_next_image");
}

function intercept_login() {
  cy.intercept("POST", `${Cypress.env("API_URL")}/login`, {
    statusCode: 204,
  }).as("login");
}

function intercept_login_with_failure() {
  cy.intercept("POST", `${Cypress.env("API_URL")}/login`, {
    statusCode: 401,
  }).as("login");
}

function login() {
  intercept_login();
  cy.visit("/");
  cy.get("input[name='username']").type("AnnotoUser#1337");
  cy.get("input[name='password']").type("test1234");
  return new Promise((resolve) => {
    cy.get("button#submit").click();
    cy.wait("@login").then(() => {
      resolve(null);
    });
  });
}

describe("Application", () => {
  it("visits the app root url", () => {
    cy.visit("/");
    cy.contains("h1", "Annoto");
  });
});

describe("LoginView", () => {
  it("logs the user in when valid login data is provided", () => {
    intercept_login();
    cy.visit("/");
    cy.get("input[name='username']").type("AnnotoUser#1337");
    cy.get("input[name='password']").type("test1234");
    cy.get("button#submit").click();
    cy.wait("@login").then(() => {
      cy.get("#task-view");
    });
  });

  it("warns if no password or username provided", () => {
    intercept_login();
    cy.visit("/");
    cy.get("button#submit").click();
    cy.get("div.alert.-warning");
  });

  it("errors if invalid login data provided", () => {
    intercept_login_with_failure();
    cy.visit("/");
    cy.get("input[name='username']").type("AnnotoUser#1337");
    cy.get("input[name='password']").type("wrong_password");
    cy.get("button#submit").click();
    cy.wait("@login").then(() => {
      cy.get("div.alert.-danger");
    });
  });
});

describe("TaskView", () => {
  it("shows username", async () => {
    await login();
    cy.get("#userLabel").contains("AnnotoUser#1337");
  });

  it("informs the user when no more images are available for annotation", async () => {
    intercept_get_task();
    intercept_next_image_with_failure();
    await login();

    cy.wait("@get_task");
    cy.wait("@get_next_image").then(() => {
      cy.get("#no-more-images").should("be.visible");
    });
  });

  it("shows annotation buttons", async () => {
    intercept_get_task();
    intercept_next_image();
    await login();

    cy.wait("@get_task").then(() => {
      cy.wait("@get_next_image").then(() => {
        cy.get("#annotation-button-atrial-fibrillation").should("be.visible");
        cy.get("#annotation-button-other").should("be.visible");
      });
    });
  });

  it("shows image display", async () => {
    intercept_get_task();
    intercept_next_image();
    await login();

    cy.wait("@get_task").then(() => {
      cy.wait("@get_next_image").then(() => {
        cy.get("#image-display").should("be.visible");
      });
    });
  });
});
