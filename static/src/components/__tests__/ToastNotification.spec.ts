import { mount } from "@vue/test-utils";
import ToastNotification from "@/components/ToastNotification.vue";

describe("ToastNotification", () => {
  it("exists", () => {
    mount(ToastNotification, {
      props: {
        message: "Test",
      },
    });
  });
});
