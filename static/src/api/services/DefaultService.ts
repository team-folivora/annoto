/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Annotation } from '../models/Annotation';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class DefaultService {

    /**
     * Get Image
     * Get the image that should be annotated
     * @param src
     * @returns binary Successful Response
     * @throws ApiError
     */
    public static getImage(
        src: string,
    ): CancelablePromise<Blob> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/images/{src}',
            path: {
                'src': src,
            },
            responseType: 'blob',
            errors: {
                404: `File not found`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Save Annotation
     * Saves the annotation for the specified image
     * @param src
     * @param requestBody
     * @returns void
     * @throws ApiError
     */
    public static saveAnnotation(
        src: string,
        requestBody: Annotation,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/images/{src}',
            path: {
                'src': src,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Bad Request`,
                404: `File not found`,
                422: `Validation Error`,
            },
        });
    }

}