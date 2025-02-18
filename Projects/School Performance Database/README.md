# Design Document

By Bin Yang

Video overview: <URL [HERE](https://youtu.be/QoUwBSxJlUU)>

## Scope

The database for CS50 SQL includes all entities necessary to facilitate the process of tracking student progress and instructors performance. As such, included in the database's scope is:

* Students, including basic identifying information
* Instructors, including basic identifying information
* courses, including basic identifying information
* grades, including students grades
* instructor_evaluation, Instructor evaluations provide specific feedback on each of these areas to help instructors understand their strengths and areas for improvement

Out of scope are elements like repeated courses, and other non-core attributes.

## Functional Requirements

* Tracking all courses of student completed
* Tracking all students degress process - the total units completed and passed by all students, along with their overall cumulative grade point average (GPA).

## Representation
Entities are captured in SQLite tables with the following schema.

### Entities
The database includes the following entities:

#### Students
The `students` table includes:

* `id`, which specifies the unique ID for the student as an `INTEGER`. This column thus has the `PRIMARY KEY` constraint applied.
* `student_id`, A `UNIQUE` constraint ensures no two students have the same student id.
* `first_name`, which specifies the student's first name as `TEXT`, given `TEXT` is appropriate for name fields.
* `last_name`, which specifies the student's last name. `TEXT` is used for the same reason as `first_name`.
* `major`, which specifies the student's major. `TEXT` is used for the same reason as `first_name`.
* `enroll_year`, which specifies when the student beroll in the university. The default value for the `enroll_year` attribute is the current strftime in Year, as denoted by `DEFAULT (strftime('%Y'))`.

All columns in the `students` table are required and hence should have the `NOT NULL` constraint applied. `enroll_year` column to indicate the `year` when the course is offered (defaults to the current year),

#### Instructors
The `instructors` table includes:

* `id`, which specifies the unique ID for the instructor as an `INTEGER`. This column thus has the `PRIMARY KEY` constraint applied.
* `first_name`, which specifies the instructor's first name as `TEXT`.
* `last_name`, which specifies the instructor's last name as `TEXT`.
* `education`, which specifies the instructor's level of eduction as `TEXT`. The eduction of instructors must be one of 'B' (Bachelor's), 'M' (Master's), or 'PhD' (Doctorate), as denoted by `CHECK ("education" IN ('B', 'M', 'PhD'))`.

All columns in the `instructors` table are required and hence should have the `NOT NULL` constraint applied. The `education` column to indicate the highest education level attained by the instructor. The `education` column has a `CHECK` constraint ensuring that the value stored in this column must be one of 'B' (Bachelor's), 'M' (Master's), or 'PhD' (Doctorate).


#### Courses
The `courses` table includes:

* `id`, which specifies the unique ID for the course as an `INTEGER`. This column thus has the `PRIMARY KEY` constraint applied.
* `course_name`, which specifies the course's name as `TEXT`.
* `course_section`, which specifies the course's section as `TEXT`. Section of the course (e.g., A, B, C).
* `instructor_id`, which specifies the instructor's id as `INTEGER`. This column thus has the `FOREIGN KEY` constraint applied, referencing the `id` column in the `instructors` table to ensure data integrity.
* `semester`, which specifies the semester of course issued as `TEXT`. Semester when the course is offered: Fall (F), Winter (W), Spring (S) as denoted by `CHECK ("semester" IN ('F', 'W', 'S'))`.
* `year`, which specifies the year of course issued as `INTEGER`. The default value for the `year` attribute is the current strftime in Year, as denoted by `DEFAULT (strftime('%Y'))`.
* `units`, which specifies the number of course's units as `INTEGER`. Number of units for the course issued by the university are 3, 6, or 9, as denoted by ` CHECK ("units" IN (3, 6, 9))`.

All columns are required and hence have the `NOT NULL` constraint applied where a `PRIMARY KEY` or `FOREIGN KEY` constraint is not. `semester` column to specify the `semester` when the course is offered (either 'F' for Fall, 'W' for Winter, or 'S' for Spring), `year` column to indicate the `year` when the course is offered (defaults to the current year), and `units` column to denote the number of `units` for the course (must be one of 3, 6, or 9).

#### Grades
The `grades` table includes:

* `id`, which specifies the unique ID for the grades as an `INTEGER`. This column thus has the `PRIMARY KEY` constraint applied.
* `course_id`, which specifies the course's id as `INTEGER`.  This column thus has the `FOREIGN KEY` constraint applied, referencing the `id` column in the `courses` table to ensure data integrity.
* `student_id`, which specifies the student's id as `INTEGER`.  This column thus has the `FOREIGN KEY` constraint applied, referencing the `student_id` column in the `students` table to ensure data integrity.
* `grade`, which specifies the student's grade as `INTEGER`. The school is using 9.0 Grading Schemes. The score is graded from 0 to 9, the student received on the course. Numeric grade assigned to the student (must be between 0 and 9), as denoted by `CHECK("grade" BETWEEN 0 AND 9)`.

All columns are required and hence have the `NOT NULL` constraint applied where a `PRIMARY KEY` or `FOREIGN KEY` constraint is not. `grade` column to store the numeric grade assigned to the student (must be between 0 and 9).

#### Instructor Evaluation
The `instructor_evaluation` table includes:

* `id`, which specifies the unique ID for the grades as an `INTEGER`. This column thus has the `PRIMARY KEY` constraint applied.
* `instructor_id`, which specifies the course's id as `INTEGER`.  This column thus has the `FOREIGN KEY` constraint applied, referencing the `id` column in the `instructors` table to ensure data integrity.
* `course_id`, which specifies the course's id as `INTEGER`.  This column thus has the `FOREIGN KEY` constraint applied, referencing the `id` column in the `courses` table to ensure data integrity.
* `student_id`, which specifies the student's id as `INTEGER`.  This column thus has the `FOREIGN KEY` constraint applied, referencing the `student_id` column in the `students` table to ensure data integrity.
* `competence`, which specifies the Rating for instructor's competence by student as `INTEGER`. Rating for instructor's competence (scale from 1 to 10), where 1 represents least and 10 represents most.  Numeric competence assigned by the student (must be between 1 and 10), as denoted by `CHECK("competence" BETWEEN 1 AND 10)`.
* `satisfactory`, which specifies the Rating for instructor's satisfactory by student as `INTEGER`. Rating for instructor's satisfactory (scale from 1 to 10), where 1 represents least and 10 represents most.  Numeric satisfactory assigned by the student (must be between 1 and 10), as denoted by `CHECK("satisfactory" BETWEEN 1 AND 10)`.
* `supportiveness`, which specifies the Rating for instructor's supportiveness by student as `INTEGER`. Rating for instructor's supportiveness (scale from 1 to 10), where 1 represents least and 10 represents most.  Numeric supportiveness supportiveness by the student (must be between 1 and 10), as denoted by `CHECK("supportiveness" BETWEEN 1 AND 10)`.
* `professionalism`, which specifies the Rating for instructor's professionalism by student as `INTEGER`. Rating for instructor's professionalism (scale from 1 to 10), where 1 represents least and 10 represents most.  Numeric professionalism assigned by the student (must be between 1 and 10), as denoted by `CHECK("professionalism" BETWEEN 1 AND 10)`.
* `comment_contents`, which specifies the comment by student as `TEXT`.

All columns except `comment_content` are required and hence have the `NOT NULL` constraint applied where a `PRIMARY KEY` or `FOREIGN KEY` constraint is not. `CHECK` constraints on `competence`, `satisfactory`, `supportiveness`, and `professionalism` columns to enforce that ratings are within the specified range of 1 to 10.

### Relationships

The below entity relationship diagram describes the relationships among the entities in the database.

![ER Diagram](diagram.png)
As detailed by the diagram:

* Instructors teach specialized courses and assign grades to students based on their performance in these courses. Students receive valuable feedback through these grades, which helps them track their learning and academic development.
* Students provide evaluations of their course instructors based on their experiences in enrolled courses. The quality of the overall course experience is influenced by the interaction between instructors and students.
* Instructors receive feedback from students, which can be used to improve teaching methods and course delivery.


## Optimizations

By creating these indexes, enhance the database's performance when executing queries that involve filtering or joining data based on the indexed columns, as SQLite can utilize these indexes to quickly locate and retrieve relevant records, reducing the query execution time and improving overall efficiency.
* It is common for users of the database to access degree process by any particular student. For this reason, Index on "student_id" column of the "students" table for efficient student lookup by ID.
* Users of the database might want to access a particular instructors performance. For this reason, Index on "id" column of the "instructors" table for efficient instructor lookup by ID
 submitted by any particular student.
* It is also common practice for a user of the database to concerned with viewing all students overall couses status or specified courses. to checking individual progress towards satisfying the requirements of their program. Index on "id" column of the "courses" table for efficient course lookup by ID. This index is useful for quickly retrieving course records based on their IDs.
* Composite index on ("course_id", "student_id") columns of the "grades" table for efficient grade lookup by course and student. This composite index is valuable for optimizing queries that involve searching for grades based on both course IDs and student IDs, such as retrieving all grades for a specific course taken by a particular student.

## Limitations

This SQL assumes that students take only one course per student and does not consider repeating courses. In many real-world situations, students can take multiple courses and may even repeat courses in different semesters or academic years. This complexity requires that the database schema be modified to handle a many-to-many relationship between students and courses, where students can take multiple courses and retake them over time.
