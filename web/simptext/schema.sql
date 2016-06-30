

drop table if exists entries;


create table entries(
id integer primary key autoincrement,
'input' text not null
);

insert into entries(input) values ('This is a demo');
