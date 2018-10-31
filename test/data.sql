--三单元
select * from lw_word where lessonid=73 order by id;
-- delete from lw_word where lessonid=73 and id <3305;
--四单元
select * from lw_word where lessonid=79;
-- delete from lw_word where lessonid=79 and id <3521;
--五单元
select * from lw_word where lessonid=85;
-- delete from lw_word where lessonid=79 and id <3521;
--六单元
select * from lw_word where lessonid=91 order by id;
-- delete from lw_word where lessonid=79 and id <3521;

select * from lw_lesson where unitid>=17 order by unitid,lessonid;
