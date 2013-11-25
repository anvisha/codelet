drop table if exists entries;
create table entries(
    phone integer primary key,
    name text not null,
    email text not null
);
