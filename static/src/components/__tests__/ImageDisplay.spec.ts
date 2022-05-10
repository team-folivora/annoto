import { mount } from "@cypress/vue";
import ImageDisplay from "@/components/ImageDisplay.vue";
import { OpenAPI } from "@/api/core/OpenAPI";
import { intercept_get_image, intercept_get_image_with_failure } from "../../../cypress/integration/utils";

beforeEach(() => {
  OpenAPI.BASE = "http://localhost:5000";
});

describe("ImageDisplay", () => {
  it("exists", () => {
    mount(ImageDisplay, {
      props: {
        taskId: "ecg-qrs-classification-physiodb",
        imageId: "sloth.jpg",
      },
    });
  });

  it("shows image", () => {
    intercept_get_image();
    mount(ImageDisplay, {
      props: {
        taskId: "ecg-qrs-classification-physiodb",
        imageId: "sloth.jpg",
      },
    }).get('img')
    .should('be.visible')
    .and(($img) => {
      // "naturalWidth" and "naturalHeight" are set when the image loads
      expect($img[0].naturalWidth).to.be.greaterThan(0)
    });
  });

  it("shows nothing if image load fails", () => {
    intercept_get_image_with_failure();
    mount(ImageDisplay, {
      props: {
        taskId: "ecg-qrs-classification-physiodb",
        imageId: "sloth.jpg",
      },
    }).get('img')
    .should('not.be.visible');
  });
});
