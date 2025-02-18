-- In this SQL file, write (and comment!) the schema of your database, including the CREATE TABLE, CREATE INDEX, CREATE VIEW, etc. statements that compose it
-- Represent students in the univeristy
CREATE TABLE "students"(
    "id" INTEGER,
    "student_id" INTEGER NOT NULL UNIQUE,
    "first_name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    "major" TEXT NOT NULL,
    "enroll_year" INTEGER NOT NULL DEFAULT (strftime('%Y')),
    PRIMARY KEY("id")
);

-- Represent instructors in the univeristy
CREATE TABLE "instructors" (
    "id" INTEGER,
    "first_name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    "education" TEXT NOT NULL CHECK ("education" IN ('B', 'M', 'PhD')),
    PRIMARY KEY("id")
);

-- Represent courses in the univeristy
CREATE TABLE "courses" (
    "id" INTEGER,
    "course_name" TEXT NOT NULL,
    "course_section" TEXT NOT NULL,
    "instructor_id" INTEGER NOT NULL,
    "semester" TEXT NOT NULL CHECK ("semester" IN ('F', 'W', 'S')),
    "year" INTEGER NOT NULL DEFAULT (strftime('%Y')),
    "units" INTEGER NOT NULL CHECK ("units" IN (3, 6, 9)),
    PRIMARY KEY("id"),
    FOREIGN KEY("instructor_id") REFERENCES "instructors"("id")
);

-- Represent grades assigned to students in the univeristy
CREATE TABLE "grades" (
    "id" INTEGER,
    "course_id" INTEGER NOT NULL,
    "student_id" INTEGER NOT NULL,
    "grade" INTEGER NOT NULL CHECK("grade" BETWEEN 0 AND 9),
    PRIMARY KEY("id"),
    FOREIGN KEY("student_id") REFERENCES "students"("student_id"),
    FOREIGN KEY("course_id") REFERENCES "courses"("id")
);

-- Represent instructors evluation by students
CREATE TABLE "instructor_evaluation" (
    "id" INTEGER,
    "instructor_id" INTEGER NOT NULL,
    "course_id" INTEGER NOT NULL,
    "student_id" INTEGER NOT NULL,
    "competence" INTEGER NOT NULL CHECK ("competence" BETWEEN '1' AND '10'),
    "satisfactory" INTEGER NOT NULL CHECK ("satisfactory" BETWEEN '1' AND '10'),
    "supportiveness" INTEGER NOT NULL CHECK ("supportiveness" BETWEEN '1' AND '10'),
    "professionalism" INTEGER NOT NULL CHECK ("professionalism" BETWEEN '1' AND '10'),
    "comment_contents" TEXT,
    PRIMARY KEY("id"),
    FOREIGN KEY("student_id") REFERENCES "students"("student_id"),
    FOREIGN KEY("instructor_id") REFERENCES "instructors"("id"),
    FOREIGN KEY("course_id") REFERENCES "courses"("id")
);

-- Represent the total units completed and passed by all students, along with their overall cumulative grade point average (GPA).
CREATE VIEW "student_process_status" AS
    SELECT "student_id", SUM("grade"*"units")/SUM("units") AS "OCGPA", SUM("units") AS "TC_Units" FROM "grades"
    JOIN "courses"
    ON "grades"."course_id" = "courses"."id"
    GROUP BY "grades"."student_id"
    HAVING "grade" >= '2';

-- Represents all the courses that students have failed.
CREATE VIEW "students_failed_courses" AS
	SELECT  "grades"."student_id","first_name","last_name","course_name" FROM "grades"
	JOIN "students"
	ON "students"."student_id" = "grades"."student_id"
	JOIN "courses"
	ON "grades"."course_id" = "courses"."id"
	WHERE "grade" < '2';

-- Represents students who have failed more than one course.
CREATE VIEW "student_academic_attention" AS
    SELECT * FROM (
        SELECT "student_id","first_name","last_name", COUNT("course_name") As "#_failed_courses" FROM "students_failed_courses"
        )
    WHERE "#_failed_courses" > 1;

-- Represents all instructors' overall performance (competence, satisfactory, supportiveness, professionalism).
CREATE VIEW "instructors_performance" AS
	SELECT "first_name", "last_name", ROUND(AVG("competence"),2) AS "competence",
	ROUND(AVG("satisfactory"),2) AS "satisfactory",
	ROUND(AVG("supportiveness"),2) AS "supportiveness",
	ROUND(AVG("professionalism"),2) AS "professionalism"
	FROM "instructor_evaluation"
	JOIN "instructors"
	ON "instructor_evaluation"."instructor_id" = "instructors"."id"
	GROUP BY "instructor_id";

-- Create indexes to speed common searches
CREATE INDEX "student_course_search" ON "courses" ("id");
CREATE INDEX "student_search" ON "students" ("student_id");
CREATE INDEX "instructor_search" ON "instructor" ("id");
CREATE INDEX "student_grades_search_by_courses_by_students" ON "grades" ("course_id","student_id");
