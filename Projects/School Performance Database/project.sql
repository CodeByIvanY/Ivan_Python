-- In this SQL file, write (and comment!) the typical SQL queries users will run on your database
-- Add a new student
INSERT INTO "students" ("student_id","first_name", "last_name", "major", "enroll_year")
VALUES
('214440444', 'Love', 'Night', 'Bcom Accounting', '2020');

-- Add a new instructor
INSERT INTO "instructors" ("first_name", "last_name", "education")
VALUES ('Bartsksz', 'Amrtski', 'M');

-- Add a new courses
INSERT INTO "courses" ("course_name", "course_section", "instructor_id", "semester", "year", "units")
VALUES
('ADMS4590 Comprehensive and Multi-subject Accounting Problems', 'P', '1', 'W', '2025', '3'),
('ADMS4590 Comprehensive and Multi-subject Accounting Problems', 'P', '1', 'W', '2025', '5'),
('ECON1280 Principles of Risk Management', 'M', '2', 'W', '2024', '3');

-- Add a new grades
INSERT INTO "grades" ("course_id", "student_id", "grade")
VALUES ('1', '214440444', '8');

-- Add a new evaluations by students
INSERT INTO "instructor_evaluation" ("instructor_id", "course_id", "student_id", "competence", "satisfactory", "supportiveness", "professionalism", "comment_contents")
VALUES ('1', '24', '214440444', '9', '8', '6', '7', 'N/A');

-- Update an individual student's program when they changed their program
UPDATE "students" SET "major" = "Bcom Finance"
WHERE "student_id" = '214440444';

-- Delete an courses when its cancelled.
DELETE FROM "courses" WHERE "id" = 2;

-- Find student's Degree Progress given student's id
SELECT * FROM "student_process_status"
WHERE "student_id" = '214440444';

-- Find student's failed courses given student id or student first and last name
SELECT * FROM "students_failed_courses"
WHERE "student_id" = '214440444' OR ("first_name" = 'Love' AND "last_name" = 'Night');

-- Find individual instructor's performance given instructor's first and last name
SELECT * FROM "instructors_performance"
WHERE "first_name" = 'Bartsksz' AND "last_name" = 'Amrtski';
