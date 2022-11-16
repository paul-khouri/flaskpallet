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
    image text,
    alttext text,
    updated_at date,
    foreign key (user_id) references user(id)
);

insert into post(title, body, user_id, created_at,image, alttext)
values(
"The Silence of Animals",
"One of the goals of psychoanalysis was the taming of morality."||
"Not only anarchic impulse but also the moral sense had to submit to reason."||
"But the dictatorship of reason could never be complete."||
"If our impulses are at war with each other they are also at war with the demands of conscience, themselves often conflicting."||
"The strength of the ego is shown not in trying to harmonise these conflicts but in learning to live with them."||
"That is part of what it means to accept a personal fate. But, for Freud, fatalism had nothing to do with passivity."|| char(10) ||
"In some ways Freud's view of human life resembles that of Arthur Schopenhauer,"||
"the nineteenth-century German philosopher of pessimism."||
"Freud claimed not to have read Schopenhauer until late in life. "||
"But he also acknowledged that Schopenhauer had anticipated the"||
"fundamental insight of psychoanalysis, writing:"||
" 'Probably very few people can have realised the momentous significance for"||
" life and science of the recognition of unconscious mental processes'.",
    1,
    datetime('now', '-2 months', '+200 minutes' , '-59 seconds'),
    "placeholder.png",
    "Place holder"
);

insert into post(title, body, user_id, created_at,image, alttext)
values(
    "The Secret Life of Salvador Dali",
 "I was to begin my secondary studies, and for this I was sent to another religious school, " ||
"that of the Marist Brothers. At this time I claimed to have made sensational discoveries "||
"in the field of mathematics which would enable me to make money. My method was simple. "||
"It was this: I would buy five-centimo pieces with ten-centimo pieces for each five that I was offered "||
"I would give ten in exchange! All the money that I could obtain from my parents I would immediately spend in this way,"||
"taking a frenzied delight in the game which was incomprehensible to everyone and inevitably ruinous."||
"One day when my father made me a present of a duro (five pesetas), I rushed out to change "||
"it into ten-centimo pieces, which made several marvellous piles! As soon as I got to "||
"school I triumphantly announced that on this very day I would open my market to buy "||
"five-centimo pieces on my usual conditions."|| char(10) ||

"So at the first recreation period I took up my post behind a little table, and with great delight "||
"I arranged the coins in several piles. All my schoolmates gathered round me, eager to realize the promised exchange. "||
"To the consternation of everyone I actually gave back ten centimos for every five I was offered! "||
"My money spent, I pretended to go over my accounts in a secret little book which I put back preciously "||
"in my pocket, securing it with several safety pins. After which I exclaimed, rubbing my hands with"||
"satisfaction, 'Again I've made a profit!' I then Got up from my counter table and strode off, "||
"not without having first cast a contemptuous glance around at my schoolmates, with an "||
"expression which poorly concealed my joy, as if to say, 'Once more I've put one over on you! What idiots!'"|| char(10) ||

"This money-buying game began to fascinate me in an obsessing way, and from then on I "||
"canalized all my activity toward obtaining as much money as possible from my "||
"parents on the most varied pretexts for buying books or paint; "||
"or else, by displaying such exemplary and unusual conduct that it warranted "||
"my asking for some monetary reward. My financial needs grew, for in order " ||
"to consolidate my prestige it was necessary for me to exchange more and more "||
"considerable sums; it was the only sure way of amplifying the sensational "||
"astonishment which steadily spread around me at each new exchange..",
    1,
    datetime('now', '-1 months', '+680 minutes', '+28 seconds'),
    "placeholder.png",
    "Place holder"
);

insert into post(title, body, user_id, created_at,image, alttext)
values(
    "The Golden Ratio",
"The association of the Golden Ratio with the pentagon, fivefold symmetry, and the Platonic solids "||
"is interesting in itself and, indeed was more than sufficient to ignite the curiosity of the ancient "||
"Greeks. The Pythagorean fascination with the pentagon and the pentagram, coupled with Plato's "||
"interest in the regular solids and his belief that the latter represented fundamental cosmic entities, "||
"prompted generations of mathematicians to labor on the formulation of numerous theorems concerning phi. "|| char(10) ||
"Yet the Golden Ratio would not have reached the level of almost reverential status that it "||
"eventually achieved were it not for some truly unique algebraic properties. In order to understand these properties, "||
"we need first to find the precise value of phi.",
    1,
    datetime('now', '-19 days', '1200 minutes', '+10 seconds'),
    "placeholder.png",
    "Place holder"
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

