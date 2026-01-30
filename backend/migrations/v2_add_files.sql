-- Add file tracking columns to job_applications table
ALTER TABLE job_applications ADD COLUMN IF NOT EXISTS resume_path VARCHAR(500);
ALTER TABLE job_applications ADD COLUMN IF NOT EXISTS resume_filename VARCHAR(200);
ALTER TABLE job_applications ADD COLUMN IF NOT EXISTS cover_letter_path VARCHAR(500);
ALTER TABLE job_applications ADD COLUMN IF NOT EXISTS cover_letter_filename VARCHAR(200);
