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
     * @param taskId
     * @param src
     * @returns binary Successful Response
     * @throws ApiError
     */
    public static getImage(
        taskId: string,
        src: string,
    ): CancelablePromise<Blob> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/tasks/{task_id}/{src}',
            path: {
                'task_id': taskId,
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
     * @param taskId
     * @param src
     * @param requestBody
     * @returns void
     * @throws ApiError
     */
    public static saveAnnotation(
        taskId: string,
        src: string,
        requestBody: AnnotationData,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/tasks/{task_id}/{src}',
            path: {
                'task_id': taskId,
                'src': src,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                400: `Hash values of the annotation and the local source do not match!`,
                404: `File not found!`,
                422: `Validation Error`,
                428: `Provided proofs are not valid!`,
            },
        });
    }

}