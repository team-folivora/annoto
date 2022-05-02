import type { CyHttpMessages } from "cypress/types/net-stubbing";

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

export function intercept_store_annotation() {
  cy.intercept(
    "POST",
    `${Cypress.env("API_URL")}/tasks/ecg-qrs-classification-physiodb/sloth.jpg`,
    cy
      .spy(
        {
          handle: (req: CyHttpMessages.IncomingHttpRequest) => {
            req.reply({ statusCode: 204 });
          },
        },
        "handle"
      )
      .as("store_annotation_spy")
  ).as("store_annotation");
}

export function intercept_get_image() {
  cy.intercept(
    "GET",
    `${Cypress.env("API_URL")}/tasks/ecg-qrs-classification-physiodb/sloth.jpg`,
    { fixture: "sloth.jpg" }
  ).as("get_image");
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

export function login(config: { [key: string]: Function } = {}) {
  config["intercept_login"] ||= intercept_login;
  config["intercept_get_task"] ||= intercept_get_task;
  config["intercept_next_image"] ||= intercept_next_image;
  config["intercept_get_image"] ||= intercept_get_image;
  config["intercept_store_annotation"] ||= intercept_store_annotation;
  config["intercept_login"]();
  config["intercept_get_task"]();
  config["intercept_next_image"]();
  config["intercept_get_image"]();
  config["intercept_store_annotation"]();
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

export function proof_condition() {
  return cy
    .get("#proof-of-condition .checkbox-label")
    .click()
    .get("#proof-of-condition button")
    .click();
}
