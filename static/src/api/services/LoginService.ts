/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { LoginData } from '../models/LoginData';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class LoginService {

    /**
     * Login
     * Validate login via username and password
     * @param requestBody
     * @returns void
     * @throws ApiError
     */
    public static login(
        requestBody: LoginData,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/login/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                401: `Failed to validate login`,
                422: `Validation Error`,
            },
        });
    }

}