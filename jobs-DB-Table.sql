Create DATABASE if not exists myjobs;
/*use myjobs;
drop TABLE if exists jobs;*/
use myjobs;
create table jobs
(
	job_ID		INT 			NOT NUll	UNIQUE AUTO_INCREMENT,
    job_title	VARCHAR(50)		NOT NULL,
    job_url		VARCHAR(100)	NOT NULL,
    job_date	DATE			NOT NULL,
    job_desc	VARCHAR(300)	NOT NULL,
    job_stage	VARCHAR(25)		NOT NULL,
    job_accepted	BOOLEAN,
    CONSTRAINT	jobs_pk PRIMARY KEY (job_ID)
);

USE myjobs; 
INSERT INTO jobs VALUES
(default, 'Python 3 Devloper', 'python.com', '2022-04-25', 'Python, MySQL', 'applied', NULL );

USE myjobs;
SELECT * From jobs  
