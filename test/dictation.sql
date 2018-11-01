select distinct word from lw_testwords where testid in (1,2);
select distinct word from lw_testwords where testid in ('1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16');

select distinct word from lw_testwords where testid in (21);

select * from lw_test where lessonid is null;

select * from lw_word where lessonid=79;
delete from lw_word where lessonid=79 and id <3521;

delete from lw_testwords;
delete from lw_test;


CREATE TABLE "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);

CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");
