import { type App, h, render, type Plugin } from "vue";
import type { ToastProps, ToastOptions, ToasterApi } from "@/plugins/types";
import ToastNotification from "@/components/ToastNotification.vue";

function createToaster(app: App, globalOptions: ToastOptions): ToasterApi {
  return {
    show(message: string, options: ToastOptions = {}) {
      const mergedOptions = { ...globalOptions, ...options };
      const props: ToastProps = { message, ...mergedOptions };

      const div = document.createElement("div");
      document.body.appendChild(div);
      const vNode = h(ToastNotification, props);
      vNode.appContext = app._context;
      render(vNode, div);
    },

    success(message: string, options: ToastOptions = {}) {
      options.type = "success";
      this.show(message, options);
    },

    danger(message: string, options: ToastOptions = {}) {
      options.type = "danger";
      this.show(message, options);
    },

    warning(message: string, options: ToastOptions = {}) {
      options.type = "warning";
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
