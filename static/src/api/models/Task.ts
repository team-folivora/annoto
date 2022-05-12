/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * A labeling task
 */
export type Task = {
    /**
     * The identifier of this labelling task
     */
    id: string;
    /**
     * A brief description of this labelling task
     */
    description: string;
    /**
     * List of labels
     */
    labels: Array<string>;
};
