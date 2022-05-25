/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { BaseTask } from '../models/BaseTask';
import type { FHIRECGAnnotationData } from '../models/FHIRECGAnnotationData';
import type { FHIRECGTask } from '../models/FHIRECGTask';
import type { ImageAnnotationData } from '../models/ImageAnnotationData';
import type { ImageTask } from '../models/ImageTask';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class TasksService {

    /**
     * Get Tasks
     * Get a list of all available labeling tasks
     * @returns BaseTask Successful Response
     * @throws ApiError
     */
    public static getTasks(): CancelablePromise<Array<BaseTask>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/tasks/',
        });
    }

    /**
     * Get Task
     * Get all information about a labelling task
     * @param taskId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getTask(
        taskId: string,
    ): CancelablePromise<(ImageTask | FHIRECGTask)> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/tasks/{task_id}',
            path: {
                'task_id': taskId,
            },
            errors: {
                404: `Task not found!`,
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Next Sample
     * Get the sample that should be annotated
     * @param taskId
     * @returns string Successful Response
     * @throws ApiError
     */
    public static getNextSample(
        taskId: string,
    ): CancelablePromise<string> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/tasks/{task_id}/next',
            path: {
                'task_id': taskId,
            },
            errors: {
                404: `No more samples to annotate`,
                422: `Validation Error`,
            },
        });
    }

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
     * Saves the annotation for the specified sample
     * @param taskId
     * @param sampleId
     * @param requestBody
     * @returns void
     * @throws ApiError
     */
    public static saveAnnotation(
        taskId: string,
        sampleId: string,
        requestBody: (ImageAnnotationData | FHIRECGAnnotationData),
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/tasks/{task_id}/{sample_id}',
            path: {
                'task_id': taskId,
                'sample_id': sampleId,
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