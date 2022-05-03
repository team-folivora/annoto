import type { Method } from "axios";
import type { CyHttpMessages, RouteMatcher } from "cypress/types/net-stubbing";

function intercept_with_spy(
  method: Method,
  url: RouteMatcher,
  response: object,
  name: string
) {
  cy.intercept(
    method,
    url,
    cy
      .spy(
        {
          handle: (req: CyHttpMessages.IncomingHttpRequest) => {
            req.reply(response);
          },
        },
        "handle"
      )
      .as(`${name}_spy`)
  ).as(name);
}

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
  intercept_with_spy(
    "POST",
    `${Cypress.env("API_URL")}/tasks/ecg-qrs-classification-physiodb/sloth.jpg`,
    { statusCode: 204 },
    "store_annotation"
  );
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

export interface InterceptConfig {
  intercept_login?: () => void;
  intercept_get_task?: () => void;
  intercept_next_image?: () => void;
  intercept_get_image?: () => void;
  intercept_store_annotation?: () => void;
}

// Make sure that every key of IntercepyConfig will be filled with a default in this object.
const defaultInterceptConfig: InterceptConfig = {
  intercept_login: intercept_login,
  intercept_get_task: intercept_get_task,
  intercept_next_image: intercept_next_image,
  intercept_get_image: intercept_get_image,
  intercept_store_annotation: intercept_store_annotation,
};

export function setup_intercepts(config: InterceptConfig = {}) {
  const interceptConfig: { [key: string]: () => void } = {
    ...defaultInterceptConfig,
    ...config,
  };
  for (const k in interceptConfig) {
    interceptConfig[k]();
  }
}

export function login() {
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
