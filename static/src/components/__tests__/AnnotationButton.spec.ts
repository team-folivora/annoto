import { mount } from "@cypress/vue";
import AnnotationButton from "@/components/AnnotationButton.vue";
import { OpenAPI } from "@/api/core/OpenAPI";
import { ElMessage } from "element-plus";
import {
  intercept_get_image,
  intercept_store_annotation,
  intercept_get_image_with_failure,
} from "../../../cypress/integration/utils";

beforeEach(() => {
  OpenAPI.BASE = "http://localhost:5000";
});

afterEach(() => {
  ElMessage.closeAll();
});

describe("AnnotationButton", () => {
  it("exists", () => {
    mount(AnnotationButton, {
      props: {
        label: "Test",
        taskId: "ecg-qrs-classification-physiodb",
        imageId: "sloth.jpg",
        competency: "Dr.",
        isAttentive: true,
        isTrained: true,
      },
    });
  });

  it("renders properly", () => {
    mount(AnnotationButton, {
      props: {
        label: "Test",
        taskId: "ecg-qrs-classification-physiodb",
        imageId: "sloth.jpg",
        competency: "Dr.",
        isAttentive: true,
        isTrained: true,
      },
    });
    cy.get("button").should("be.visible");
  });

  it("is not disabled", () => {
    mount(AnnotationButton, {
      props: {
        label: "Test",
        taskId: "ecg-qrs-classification-physiodb",
        imageId: "sloth.jpg",
        competency: "Dr.",
        isAttentive: true,
        isTrained: true,
      },
    });
    cy.get("button").should("not.be.disabled");
  });

  it("shows specific label", () => {
    const label = "Cypress";
    mount(AnnotationButton, {
      props: {
        label: label,
        taskId: "ecg-qrs-classification-physiodb",
        imageId: "sloth.jpg",
        competency: "Dr.",
        isAttentive: true,
        isTrained: true,
      },
    });
    cy.get("button").contains(label);
  });

  it("sends request when clicked and shows success message", () => {
    intercept_get_image();
    intercept_store_annotation();
    mount(AnnotationButton, {
      props: {
        label: "Test",
        taskId: "ecg-qrs-classification-physiodb",
        imageId: "sloth.jpg",
        competency: "Dr.",
        isAttentive: true,
        isTrained: true,
      },
    });
    cy.get("button")
      .click()
      .wait("@get_image")
      .wait("@store_annotation")
      .get("@store_annotation_spy")
      .should("be.called")
      .get("html")
      .contains("Annotation successfully saved");
  });

  it("shows failure message on saving failure", () => {
    intercept_get_image_with_failure();
    mount(AnnotationButton, {
      props: {
        label: "Test",
        taskId: "ecg-qrs-classification-physiodb",
        imageId: "sloth.jpg",
        competency: "Dr.",
        isAttentive: true,
        isTrained: true,
      },
    });
    cy.get("button")
      .click()
      .wait("@get_image")
      .get("html")
      .contains("Something went wrong");
  });
});
