import {
  openTask,
  interceptNextImageWithFailure,
  login,
  proofCondition,
  setupIntercepts,
} from "./utils";
import {task} from "../fixtures/fixture_objects";

describe("TaskView", () => {
  it("shows full name", () => {
    setupIntercepts();
    login()
      .then(() => openTask(task.id))
      .get("#userLabel")
      .contains("Prof. Dr. Folivora");
  });

  it("shows the proof of condition popup on startup", () => {
    setupIntercepts();
    login()
      .then(() => openTask(task.id))
      .get("#proof-of-condition")
      .should("be.visible");
  });

  it("can close the proof of condition dialog when checkbox is checked", () => {
    setupIntercepts();
    login()
      .wait("@get_tasks")
      .then(() => openTask(task.id))
      .then(proofCondition)
      .get("#proof-of-condition")
      .should("not.be.visible");
  });

  it("cannot close the proof of condition dialog when checkbox is not checked", () => {
    setupIntercepts();
    login()
      .then(() => openTask(task.id))
      .get("#proof-of-condition button")
      .click({ force: true })
      .get("#proof-of-condition")
      .should("be.visible");
  });

  it("informs the user when no more images are available for annotation", () => {
    setupIntercepts({
      interceptNextImage: interceptNextImageWithFailure,
    });
    login()
      .wait("@get_tasks")
      .then(() => openTask(task.id))
      .wait("@get_next_image")
      .get("#no-more-images")
      .should("be.visible");
  });

  it("shows annotation buttons", () => {
    setupIntercepts();
    login()
      .wait("@get_tasks")
      .then(() => openTask(task.id))
      .wait("@get_next_image")
      .get("#annotation-button-atrial-fibrillation")
      .should("be.visible")
      .get("#annotation-button-other")
      .should("be.visible");
  });

  it("shows image display", () => {
    setupIntercepts();
    login()
      .wait("@get_tasks")
      .then(() => openTask(task.id))
      .wait("@get_next_image")
      .get("#image-display")
      .should("be.visible");
  });

  it("annotation button stores annotation", () => {
    setupIntercepts();
    login()
      .wait("@get_tasks")
      .then(() => openTask(task.id))
      .then(proofCondition)
      .wait("@get_next_image")
      .get("#annotation-button-atrial-fibrillation")
      .click()
      .wait("@store_annotation")
      .get("@store_annotation_spy")
      .its("args.0.0.body")
      .should("deep.include", { is_attentive: true });
  });

  it("annotation request includes condition from popup", () => {
    cy.on("uncaught:exception", () => false);
    setupIntercepts();
    login()
      .wait("@get_tasks")
      .then(() => openTask(task.id))
      .wait("@get_next_image")
      .get("#annotation-button-atrial-fibrillation")
      .click({ force: true })
      .wait("@store_annotation")
      .get("@store_annotation_spy")
      .its("args.0.0.body")
      .should("deep.include", { is_attentive: false });
  });

  it("shows next image once annotation has been made", () => {
    setupIntercepts();
    login()
      .wait("@get_tasks")
      .then(() => openTask(task.id))
      .then(proofCondition)
      .wait("@get_next_image")
      .get("#annotation-button-atrial-fibrillation")
      .click()
      .wait("@get_next_image")
      .get("#image-display")
      .should("be.visible");
  });
});
