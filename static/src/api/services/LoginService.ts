/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { LoginRequest } from '../models/LoginRequest';
import type { LoginResponse } from '../models/LoginResponse';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class LoginService {

    /**
     * Login
     * Validate login via email and password
     * @param requestBody
     * @returns LoginResponse Successful Response
     * @throws ApiError
     */
    public static login(
        requestBody: LoginRequest,
    ): CancelablePromise<LoginResponse> {
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