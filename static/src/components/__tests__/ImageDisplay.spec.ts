import { mount } from "@cypress/vue";
import ImageDisplay from "@/components/ImageDisplay.vue";

describe("ImageDisplay", () => {
  it("exists", () => {
    mount(ImageDisplay, {
      props: {
        taskId: "ecg-qrs-classification-physiodb",
        imageId: "sloth.jpg",
      },
    });
  });
});
