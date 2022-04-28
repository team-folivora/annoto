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
  return cy
    .visit("/")
    .get("input[name='username']")
    .type("AnnotoUser#1337")
    .get("input[name='password']")
    .type("test1234")
    .get("button#submit")
    .click()
    .wait("@login");
}

describe("Application", () => {
  it("visits the app root url", () => {
    cy.visit("/").contains("h1", "Annoto");
  });
});

describe("LoginView", () => {
  it("logs the user in when valid login data is provided", () => {
    intercept_login();
    cy.visit("/")
      .get("input[name='username']")
      .type("AnnotoUser#1337")
      .get("input[name='password']")
      .type("test1234")
      .get("button#submit")
      .click()
      .wait("@login")
      .get("#task-view");
  });

  it("warns if no password or username provided", () => {
    cy.visit("/").get("button#submit").click().get("div.alert.-warning");
  });

  it("errors if invalid login data provided", () => {
    intercept_login_with_failure();
    cy.visit("/")
      .get("input[name='username']")
      .type("AnnotoUser#1337")
      .get("input[name='password']")
      .type("wrong_password")
      .get("button#submit")
      .click()
      .wait("@login")
      .get("div.alert.-danger");
  });
});

describe("TaskView", () => {
  it("shows username", () => {
    login().get("#userLabel").contains("AnnotoUser#1337");
  });

  it("informs the user when no more images are available for annotation", () => {
    intercept_get_task();
    intercept_next_image_with_failure();
    login()
      .wait("@get_task")
      .wait("@get_next_image")
      .get("#no-more-images")
      .should("be.visible");
  });

  it("shows annotation buttons", () => {
    intercept_get_task();
    intercept_next_image();
    login()
      .wait("@get_task")
      .wait("@get_next_image")
      .get("#annotation-button-atrial-fibrillation")
      .should("be.visible")
      .get("#annotation-button-other")
      .should("be.visible");
  });

  it("shows image display", () => {
    intercept_get_task();
    intercept_next_image();
    login()
      .wait("@get_task")
      .wait("@get_next_image")
      .get("#image-display")
      .should("be.visible");
  });
});
