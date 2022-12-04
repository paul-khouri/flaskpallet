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
    user_id integer primary key autoincrement not null,
    username text not null,
    password text not null,
    email text not null unique,
    created_at date not null,
    permission integer not null
);

/* create user 1 , to be updated when initialisation runs */

insert into user( username , password, email, created_at , permission)
values('admin', 'temp','a@b.com' ,datetime('now', '-3 months'), 0);
insert into user( username , password,email, created_at , permission)
values('mary', 'temp', 'c@b.com',datetime('now', '-3 months'), 1);
insert into user( username , password,email, created_at , permission)
values('jo', 'temp', 'd@b.com',datetime('now', '-6 months'), 1);

/*server install: loop through users to hash passwords */


create table post(
    post_id integer primary key autoincrement not null,
    title text not null,
    body text not null,
    user_id integer not null,
    created_at date not null,
    image text,
    alttext text,
    updated_at date,
    foreign key (user_id) references user(user_id)
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
    "secret_life.jpg",
    "Bookcover with Salvador Dali drawing of a witch"
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
    "golden_ratio.jpg",
    "Black book cover with nautilus shell spiral"
);

insert into post(title, body, user_id, created_at,image, alttext)
values(
"Exile and the Kingom",
"From east to west, in fact, her gaze swept slowly, without encountering a single obstacle, along a perfect curve. "||
"Beneath her, the blue-and-white terraces of the Arab town overlapped one another, splattered with the dark-red "||
"spots of peppers drying in the sun. Not a soul could be seen, but from the inner courts, together with the "||
"aroma of roasting coffee, there rose laughing voices or incomprehensible stamping of feet. Farther off, "||
"the palm grove, divided into uneven squares by clay walls, rustled its upper foliage in a wind that could "||
"not be felt up on the terrace. Still farther off and all the way to the horizon extended the ochre-and-grey "||
"realm of stones, in which no life was visible. At some distance from the oasis, however, near the wadi that "||
"bordered the palm grove on the west could be seen broad black tents. All around them a flock of motionless dromedaries, "||
"tiny at that distance, formed against the grey ground the black signs of a strange hand-writing, the meaning of "||
"which had to be deciphered. Above the desert, the silence was as vast as the space."|| char(10) ||
"Janine, leaning her whole body against the parapet, was speechless, unable to tear herself away from the void opening before her. "||
"Beside her, Marcel was getting restless. He was cold; he wanted to go back down. What was there to see here, after all? "||
"But she could not take her gaze from the horizon. Over yonder, still farther south, at that point where sky and earth met "||
"in a pure line - over yonder it suddenly seemed there was awaiting her something of which, though it had always been lacking, "||
"she had never been aware until now. In the advancing afternoon the light relaxed and softened; it was passing from the crystalline to the liquid."|| char(10) ||
"Simultaneously, in the heart of a woman brought there by pure chance a knot tightened by the years, habit, and boredom was slowly "||
"loosening. She was looking at the nomads' encampment. She had not even seen the men living in it; nothing was stirring among the "||
"black tents, and yet she could think only of them whose existence she had barely known until this day. Homeless, cut off "||
"from the world, they were a handful wandering over the vast territory she could see, which however was but a paltry part "||
"of an even greater expanse whose dizzying course stopped only thousands of miles farther south, where the first river "||
"finally waters the forest. Since the beginning of time, on the dry earth of this limitless land scraped to the bone, a few "||
"men had been ceaselessly trudging, possessing nothing but serving no one, poverty-stricken but free lords of a strange kingdom. "||
"Janine did not know why this thought filled her with such a sweet, vast melancholy that it closed her eyes. She knew that this "||
"kingdom had been eternally promised her and yet that it would never be hers, never again, except in this fleeting moment "||
"perhaps when she opened her eyes again on the suddenly motionless sky and on its waves of steady light, while the voices "||
"rising from the Arab town suddenly fell silent. It seemed to her that the world's course had just stopped and that, from "||
"that moment on, no one would ever age any more or die. Everywhere, henceforth, lite was suspended - except in her heart, "||
"where, at the same moment, someone was weeping with affliction and wonder.",
   2,
    datetime('now', '-19 days', '1200 minutes', '+10 seconds'),
    "placeholder.png",
    "Placeholder"
);

insert into post(title, body, user_id, created_at,image, alttext)
values(
"The Idiot", 
"At about nine o'clock one morning, at the end of November, during a thaw, a train of the St Petersburg-Warsaw "||
"line was approaching St Petersburg at full steam. Such were the damp and the fog that it was a while before "||
"daylight broke; at ten yards to the right and the left of the track it was hard to make out anything "||
"at all from the windows of the carriage. The passengers included some returning from abroad; but "||
"the third-class compartments were the most crowded, with ordinary folk and those on business, "||
"who had not travelled far. Everyone, as is usually the case, was tired, with eyes heavy after "||
"the night, everyone was cold, every face was pale yellow, the colour of the fog.",
   2,
    datetime('now', '-19 days', '1200 minutes', '+10 seconds'),
    "placeholder.png",
    "Placeholder"
);

insert into post(title, body, user_id, created_at,image, alttext)
values(
"The Battle For Spain. The Spanish Civil War 1936-1939",
"including a large derachment of the local Falange. Among the dignitaries on the stage sat Franco's wife, "||
"the Bishop of Salamanca who had issued the pastoral letter, General Millan Astray, the Founder of the "||
"Foreign Legion, and Miguel de Unamuno, the Basque philosopher who was the rector of the university. "||
"Unamuno had been exasperated by the Republic, so in the beginning he had supported the nationalist rising."||
"But he could not ignore the slaughter in this city where the infamous Major Doval from the Asturian "||
"repression was in charge, nor the murder of his friends Casto Prieto, the mayor of Salamanca, "||
"Salvador Vila, the professor of Arabic and Hebrew at the University of Granada, and of Garcia Lorca."|| char(10) ||
"Soon after the ceremony began, Professor Francisco Maldonado launched a violent attack against "||
"Catalan and Basque nationalism, which he described as the ‘cancer of the nation', "||
"which must be cured with the scalpel of fascism. At the back of the hall, somebody yelled the Legion "||
"battlecry of 'Viva la Muerte!' (Long live Death!). General Millan Astray, who looked the very "||
"spectre of war with only one arm and one eye, stood up to shout the same cry. Falangists chanted "||
"their Vivas!, arms raised in the fascist salute towards the portrait of General Franco hanging "||
"above where his wife sat."|| char(10) ||
"The noise died as Unamuno stood up slowly. His quiet voice was an impressive contrast. "||
"'All of you await my words. You know me and are aware that I am unable to remain silent. "||
"At times to be silent is to lie. For silence can be interpreted as acquiescence. I want "||
"to comment on the speech, to give it that name, of Professor Maldonado. Let us waive the "||
"personal affront implied in the sudden outburst of vituperation against the Basques and "||
"Catalans. I was myself, of course, born in Bilbao. The bishop, whether he likes it or "||
"not, is a Catalan from Barcelona. Just now I heard a necrophilous and senseless cry: "||
"'Long live Death!' And I, who have spent my life shaping paradoxes, must tell you "||
"as an expert authority that this outlandish paradox is repellent to me. General "||
"Millan Astray is a cripple. Let it be said without any undertone. He is a war invalid. "||
"So was Cervantes."||char(10) ||
"‘Unfortunately there are all too many cripples in Spain now. And soon there will "||
"be even more of them if God does not come to our aid. It pains me to think that "||
"General Millan Astray should dictate the pattern of mass psychology. A cripple "||
"who lacks the greatness of Cervantes is wont to seek ominous relief in causing "||
"mutilation around him. General Millan Astray would like to create Spain anew, a "||
"negative creation in his own image and likeness; for that reason he wishes to "||
"see Spain crippled as he unwittingly made clear.’"||char(10) ||
"The general was unable to contain his almost inarticulate fury any longer. "||
"He could only scream Muera la inteligencia!, Viva la Muerte! (Death to the intelligentsia! Long live Death!)."||
"The Falangists took up his cry and army officers took out their pistols. Apparently, "||
"the general's bodyguard even levelled his submachine-gun at Unamuno's head, but this "||
"did not deter Unamuno from crying defiance."||char(10) ||
"‘This is the temple of the intellect and I am its high priest. It is you "||
"who profane its sacred precincts. You will win, because you have more than "||
"enough brute force. But you will not convince. For to persuade you would need "||
"what you lack: reason and right in your struggle. I consider it futile to exhort you "||
"to think of Spain.’"||char(10) ||
"He paused and his arms fell to his sides. He finished in a quiet resigned tone: "||
"I have done. It would seem that the presence of Franco's wife saved him from being "||
"lynched on the spot, though when her husband was informed of what had happened he "||
"apparently wanted Unamuno to be shot. This course was not followed because of "||
"the philosopher's international reputation and the reaction caused abroad by "||
"Lorca's murder. But Unamuno died some ten weeks later, broken-hearted and cursed"||
"as a 'red' and a traitor by those he had thought were his friends.",
   2,
    datetime('now', '-19 days', '1200 minutes', '+10 seconds'),
    "placeholder.png",
    "Placeholder"
    );





create table comment(
    comment_id integer primary key autoincrement not null,
    post_id integer not null,
    created_at date not null,
    user_id text not null,
    text text not null,
    updated_at date,
    foreign key (post_id) references post(post_id)
);

insert into comment(post_id, created_at, user_id, text)
values(
    1,
    datetime('now', '-10 days', '+820 minutes', '+0 seconds'),
    3,
    "This is Jo's contribution"
);

insert into comment(post_id, created_at, user_id, text)
values(
    1,
    datetime('now', '-10 days', '+820 minutes', '+0 seconds'),
    2,
    "This is Mary's contribution"
);

insert into comment(post_id, created_at, user_id, text)
values(
    1,
    datetime('now', '-9 days', '+50 minutes', '+2 seconds'),
    2,
    "This is another Mary's contribution"
);

insert into comment(post_id, created_at, user_id, text)
values(
    2,
    datetime('now', '-9 days', '+50 minutes', '+2 seconds'),
    3,
    "This is another Jo's contribution"
);

