/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Task } from '../models/Task';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class TasksService {

    /**
     * Get Tasks
     * Get a list of the IDs of all available labelling tasks
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getTasks(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/tasks/',
        });
    }

    /**
     * Get Task
     * Get all information about a labelling task
     * @param taskId
     * @returns Task Successful Response
     * @throws ApiError
     */
    public static getTask(
        taskId: string,
    ): CancelablePromise<Task> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/tasks/{task_id}',
            path: {
                'task_id': taskId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}