/**
 * Shared types for Brasaland project modules.
 * These compact types support the reusable candidate-related helpers.
 */

export type Id = string;

export type CandidateStatus =
  | 'received'
  | 'in_progress'
  | 'selected'
  | 'discarded';

export type CandidateStage =
  | 'pending'
  | 'review'
  | 'personal_interview'
  | 'technical_interview'
  | 'offer_presented';

export interface CandidateSummaryRow {
  id?: Id;
  name?: string;
  status?: CandidateStatus | string;
  stage?: CandidateStage | string;
  notes_count?: number;
}

export interface BaseEntity {
  id: Id;
  createdAt?: string;
  updatedAt?: string;
}
