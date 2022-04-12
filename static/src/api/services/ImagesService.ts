/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AnnotationData } from '../models/AnnotationData';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class ImagesService {

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
        requestBody: AnnotationData,
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
                400: `Hash values of the annotation and the local source do not match!`,
                404: `File not found!`,
                406: `Provided username is not valid!`,
                422: `Validation Error`,
                428: `Provided proofs are not valid!`,
            },
        });
    }

}