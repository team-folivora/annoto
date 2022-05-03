/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * The fields required to create a new user
 */
export type CreateUserRequest = {
    /**
     * The name of the user
     */
    username: string;
    /**
     * The email of the user
     */
    email: string;
    /**
     * The password of the user
     */
    password: string;
};
