/**
*Database creation script
*/
/* destroy all tables */
drop table if exists user;
drop table if exists post;
drop table if exists comment;

/* enable foreign key constraint */
pragma foreign_keys = on;



create table user(
    id integer primary key autoincrement not null,
    username text not null,
    password text not null,
    created_at date not null,
    is_enabled boolean not null default true
);

/* create user 1 , to be updated when initialisation (php) runs */
insert into user( username , password, created_at , is_enabled)
values('admin', 'unhashed password', datetime('now', '-3 months'), 0);




create table post(
    id integer primary key autoincrement not null,
    title text not null,
    body text not null,
    user_id integer not null,
    created_at date not null,
    updated_at date,
    foreign key (user_id) references user(id)
);

insert into post(title, body, user_id, created_at)
values(
    "Here is our first post",
    "This is the body text for the first post.

    It is split into paragraphs.",
    1,
    datetime('now', '-2 months', '+200 minutes' , '-59 seconds')
);

insert into post(title, body, user_id, created_at)
values(
    "Here is our second post",
    "This is the body text for the second post.

    It is split into paragraphs.",
    1,
    datetime('now', '-1 months', '+680 minutes', '+28 seconds')
);

insert into post(title, body, user_id, created_at)
values(
    "Here is our third post",
    "This is the body text for the third post.

    It is split into paragraphs.",
    1,
    datetime('now', '-19 days', '1200 minutes', '+10 seconds')
);




create table comment(
    id integer primary key autoincrement not null,
    post_id integer not null,
    created_at date not null,
    name text not null,
    website text,
    text text not null,
    foreign key (post_id) references post(id)
);

insert into comment(post_id, created_at, name, website, text)
values(
    1,
    datetime('now', '-10 days', '+820 minutes', '+0 seconds'),
    'Jimmy',
    'http://google.com',
    "This is Jimmy's contribution"
);

insert into comment(post_id, created_at, name, website, text)
values(
    1,
    datetime('now', '-10 days', '+900 minutes', '+1 seconds'),
    'Jane',
    'http://msn.com',
    "This is Jane's contribution"
);

insert into comment(post_id, created_at, name, website, text)
values(
    1,
    datetime('now', '-9 days', '+50 minutes', '+2 seconds'),
    'Johnny',
    'http://yahoo.com',
    "This is Johnny's contribution"
);

insert into comment(post_id, created_at, name, website, text)
values(
    1,
    datetime('now', '-8 days', '+350 minutes', '+3 seconds'),
    'Alice',
    'http://bing.com',
    "This is Alices's contribution"
);

