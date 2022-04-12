import { type App, h, render, type Plugin } from "vue";
import type { ToasterApi } from "@/types";
import type { ToastProps, ToastOptions } from "@/types";
import ToastNotification from "../components/ToastNotification.vue";

declare module "vue" {
  interface ComponentCustomProperties {
    $toast: ToasterApi;
  }
}

function createToaster(app: App, globalOptions: ToastOptions): ToasterApi {
  return {
    show(message: string, options: ToastOptions = {}) {
      const mergedOptions = { ...globalOptions, ...options };
      const props: ToastProps = { message, ...mergedOptions };
      const div = document.createElement("div");
      document.body.appendChild(div);
      const vNode = h(ToastNotification, props);
      if (app && app._context) {
        vNode.appContext = app._context;
      }
      render(vNode, div);
      setTimeout(() => {
        // The Toast just manages hiding itself but will get removed from the DOM here
        if (div) {
          render(null, div);
          document.body.removeChild(div);
        }
      }, (options.duration?.valueOf() || 3000) + 1000);
    },

    success(message: string, options: ToastOptions = {}) {
      options.type = "success";
      this.show(message, options);
    },

    danger(message: string, options: ToastOptions = {}) {
      options.type = "danger";
      this.show(message, options);
    },

    info(message: string, options: ToastOptions = {}) {
      options.type = "info";
      this.show(message, options);
    },
  };
}

const Toaster: Plugin = {
  install(app: App, options: ToastOptions = {}) {
    app.config.globalProperties.$toast = createToaster(app, options);
  },
};

export default Toaster;
