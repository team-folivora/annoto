import type { Method } from "axios";
import type { CyHttpMessages, RouteMatcher } from "cypress/types/net-stubbing";
import { task, accessToken } from "../fixtures/fixture_objects";

function interceptWithSpy(
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

export function interceptGetTask() {
  cy.intercept("GET", `${Cypress.env("API_URL")}/tasks/${task.id}`, task).as(
    "get_task"
  );
}

export function interceptGetTasks() {
  cy.intercept("GET", `${Cypress.env("API_URL")}/tasks`, [task]).as(
    "get_tasks"
  );
}

export function interceptTetTasksWithEmptyList() {
  cy.intercept("GET", `${Cypress.env("API_URL")}/tasks`, []).as("get_tasks");
}

export function interceptNextImage() {
  cy.intercept("GET", `${Cypress.env("API_URL")}/tasks/${task.id}/next`, {
    body: "sloth.jpg",
    headers: {
      "Content-Type": "text/plain",
    },
  }).as("get_next_image");
}

export function interceptNextImageWithFailure() {
  cy.intercept("GET", `${Cypress.env("API_URL")}/tasks/${task.id}/next`, {
    statusCode: 404,
  }).as("get_next_image");
}

export function interceptStoreAnnotation() {
  interceptWithSpy(
    "POST",
    `${Cypress.env("API_URL")}/tasks/${task.id}/sloth.jpg`,
    { statusCode: 204 },
    "store_annotation"
  );
}

export function interceptGetImage() {
  cy.intercept("GET", `${Cypress.env("API_URL")}/tasks/${task.id}/sloth.jpg`, {
    fixture: "sloth.jpg",
  }).as("get_image");
}

export function interceptLogin() {
  cy.intercept("POST", `${Cypress.env("API_URL")}/login`, {
    access_token: accessToken,
  }).as("login");
}

export function interceptPing() {
  cy.intercept("GET", `${Cypress.env("API_URL")}/ping`, {
    statusCode: 204,
  }).as("ping");
}

export function interceptLoginWithFailure() {
  cy.intercept("POST", `${Cypress.env("API_URL")}/login`, {
    statusCode: 401,
  }).as("login");
}

export interface InterceptConfig {
  interceptLogin?: () => void;
  interceptPing?: () => void;
  interceptGetTask?: () => void;
  interceptGetTasks?: () => void;
  interceptNextImage?: () => void;
  interceptGetImage?: () => void;
  interceptStoreAnnotation?: () => void;
}

// Make sure that every key of IntercepyConfig will be filled with a default in this object.
const defaultInterceptConfig: InterceptConfig = {
  interceptLogin: interceptLogin,
  interceptPing: interceptPing,
  interceptGetTask: interceptGetTask,
  interceptGetTasks: interceptGetTasks,
  interceptNextImage: interceptNextImage,
  interceptGetImage: interceptGetImage,
  interceptStoreAnnotation: interceptStoreAnnotation,
};

export function setupIntercepts(config: InterceptConfig = {}) {
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
    .get("input[name='email']")
    .type("team@folivora.online")
    .get("input[name='password']")
    .type("test1234")
    .get("button#submit")
    .click()
    .wait("@login");
}

export function openTask(task_id: string) {
  return cy.visit("/").get(`.card#task-${task_id} button`).click();
}

export function proofCondition() {
  return cy
    .get("#proof-of-condition .checkbox-label")
    .click()
    .get("#proof-of-condition button")
    .click();
}
