/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { User } from '../models/User';
import type { UserCreate } from '../models/UserCreate';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class UsersService {

    /**
     * Read User
     * Read a user by their ID
     * @param userId
     * @returns User Successful Response
     * @throws ApiError
     */
    public static readUser(
        userId: number,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/users/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                404: `User not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Create User
     * Create a user
     * @param requestBody
     * @returns User Successful Response
     * @throws ApiError
     */
    public static createUser(
        requestBody: UserCreate,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/users/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Email already registered`,
                422: `Validation Error`,
            },
        });
    }

}