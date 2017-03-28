drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  inputs text not null,
  words text not null,
  level text not null,
  algs text not null,
  cselect text not null,
  s1 text not null,
  s2 text not null
);

drop table if exists params;
create table params (
  id integer primary key autoincrement,
  words text not null,
  level text not null,
  algs text not null,
  cselect text not null
);