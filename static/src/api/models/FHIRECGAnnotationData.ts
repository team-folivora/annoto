/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

/**
 * The basic Annotation Data for a data file
 */
export type FHIRECGAnnotationData = {
    /**
     * The competencies the annotator has
     */
    competency: string;
    /**
     * Whether the annotator said he finished the training
     */
    is_trained: boolean;
    /**
     * Whether the annotator said that he is attentive
     */
    is_attentive: boolean;
};
