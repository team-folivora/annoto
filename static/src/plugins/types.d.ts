declare module "vue" {
  interface ComponentCustomProperties {
    $toast: ToasterApi;
    $store: StoreApi;
  }
}

export interface ToastOptions {
  type?: "success" | "danger" | "warning" | "info";
  duration?: number;
  dismissable?: boolean;
}

export interface ToastProps extends ToastOptions {
  message: string;
}

export interface ToasterApi {
  /**
   * Shows a new ToastNotification with the given message.
   * @param message The text that should be displayed in the ToastNotification.
   * @param options The options that should be used to configure the ToastNotification.
   */
  show: (message: string, options?: ToastOptions) => void;

  /**
   * Shows a new ToastNotification with the given message and a success type.
   * @param message The text that should be displayed in the ToastNotification.
   * @param options The options that should be used to configure the ToastNotification.
   */
  success: (message: string, options?: ToastOptions) => void;

  /**
   * Shows a new ToastNotification with the given message and a danger type.
   * @param message The text that should be displayed in the ToastNotification.
   * @param options The options that should be used to configure the ToastNotification.
   */
  danger: (message: string, options?: ToastOptions) => void;

  /**
   * Shows a new ToastNotification with the given message and a warning type.
   * @param message The text that should be displayed in the ToastNotification.
   * @param options The options that should be used to configure the ToastNotification.
   */
  warning: (message: string, options?: ToastOptions) => void;

  /**
   * Shows a new ToastNotification with the given message and an info type.
   * @param message The text that should be displayed in the ToastNotification.
   * @param options The options that should be used to configure the ToastNotification.
   */
  info: (message: string, options?: ToastOptions) => void;
}

export interface StoreApi {
  /**
   * Internal jwt token.
   */
  _jwt: string | undefined;

  /**
   * VueCookies instance.
   */
  $cookies: VueCookies | undefined;

    /**
     * Indicates if the user is logged in.
     */
  isLoggedIn: boolean;

  /**
   * Initialize the store
   * @param cookies VueCookies instance
   */
  initialize(cookies: VueCookies): void;

  /**
   * Returns the current jwt token.
   */
  get jwt(): string | undefined;

  /**
   * Sets the current jwt token.
   */
  set jwt(newJWT: string | undefined): void;
}
