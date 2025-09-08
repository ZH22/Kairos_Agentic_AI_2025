-- Add seller_email column to listings table
-- Run this SQL command in your Supabase SQL editor

ALTER TABLE listing ADD COLUMN seller_email TEXT;

-- Optional: Add a comment to document the column
COMMENT ON COLUMN listing.seller_email IS 'Contact email provided by seller for direct buyer communication';