/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { TaskType } from './TaskType';

/**
 * A labeling task
 */
export type BaseTask = {
    /**
     * The type of the task
     */
    type_id: TaskType;
    /**
     * The identifier of this labelling task
     */
    id: string;
    /**
     * A brief description of this labelling task
     */
    description: string;
};
