

drop table if exists entries;
drop table if exists rets;

create table entries(
id integer primary key autoincrement,
'input' text not null
);

create table rets(
id integer primary key autoincrement,
'output' text
);