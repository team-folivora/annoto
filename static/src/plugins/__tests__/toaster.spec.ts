import { createApp } from "vue";
import Toaster from "../toaster";

describe("Toast plugin", () => {
  it("works as plugin", () => {
    const app = createApp({});

    app.use(Toaster);
    app.mount("body");
    app.config.globalProperties.$toast.success("test message", {
      duration: 1,
    });

    expect(document.body.querySelectorAll("div > div#container").length).equal(
      1
    );
  });
});
