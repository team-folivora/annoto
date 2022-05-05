/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class PingService {

    /**
     * Ping
     * @returns void
     * @throws ApiError
     */
    public static ping(): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/ping/',
        });
    }

}