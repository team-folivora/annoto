export function intercept_get_task() {
  cy.intercept(
    "GET",
    `${Cypress.env("API_URL")}/tasks/ecg-qrs-classification-physiodb`,
    { fixture: "task.json" }
  ).as("get_task");
}

export function intercept_next_image() {
  cy.intercept(
    "GET",
    `${Cypress.env("API_URL")}/tasks/ecg-qrs-classification-physiodb/next`,
    {
      fixture: "nextImage.txt",
    }
  ).as("get_next_image");
}

export function intercept_next_image_with_failure() {
  cy.intercept(
    "GET",
    `${Cypress.env("API_URL")}/tasks/ecg-qrs-classification-physiodb/next`,
    { statusCode: 404 }
  ).as("get_next_image");
}

export function intercept_login() {
  cy.intercept("POST", `${Cypress.env("API_URL")}/login`, {
    statusCode: 204,
  }).as("login");
}

export function intercept_login_with_failure() {
  cy.intercept("POST", `${Cypress.env("API_URL")}/login`, {
    statusCode: 401,
  }).as("login");
}

export function login() {
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
