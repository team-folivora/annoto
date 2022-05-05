/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * Login token (JWT) and full user name
 */
export type LoginResponse = {
    /**
     * The generated JWT access token
     */
    access_token: string;
    /**
     * The fullname of the user
     */
    fullname: string;
};
