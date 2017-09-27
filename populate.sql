-- users table

-- password is quakt
INSERT INTO users(username, bio, password_hash, credits) VALUES(
    'meetmangukiya',
    'aka mangu(forcefully :( ); handles backend',
    '\\x78dd6f42eda97bc075aa0ce4d5ddf1a042c246bb'::bytea,
    100
);

INSERT INTO users(username, bio, password_hash, credits) VALUES(
    'chintan.gm',
    'aka chinzzz; handles database, our rookie DBA :P',
    '\\x78dd6f42eda97bc075aa0ce4d5ddf1a042c246bb'::bytea,
    50
);

INSERT INTO users(username, bio, password_hash, credits) VALUES(
    'raj.mm',
    'aka raj(:/); handles frontend',
    '\\x78dd6f42eda97bc075aa0ce4d5ddf1a042c246bb'::bytea,
    1000
);

INSERT INTO users(username, bio, password_hash, credits) VALUES(
    'vignesh.vaid',
    'aka jignesh; handles <unknown>',
    '\\x78dd6f42eda97bc075aa0ce4d5ddf1a042c246bb'::bytea,
    345
);

-- salts TABLE
INSERT INTO salts(salt, username) VALUES('quast', 'meetmangukiya');
INSERT INTO salts(salt, username) VALUES('quast', 'vignesh.vaid');
INSERT INTO salts(salt, username) VALUES('quast', 'chintan.gm');
INSERT INTO salts(salt, username) VALUES('quast', 'raj.mm');

-- questions TABLE

INSERT INTO questions(title, description, author, upvotes, downvotes, qid) VALUES(
    'Why should we use java for our backend?', '',
    'meetmangukiya', 10, 2, 1
);

INSERT INTO questions(title, description, author, upvotes, downvotes, qid) VALUES(
    'Why is there no angular 3?', '',
    'raj.mm', 109, 0, 2
);

-- answers TABLE

INSERT INTO answers(body, upvotes, downvotes, author, qid) VALUES(
    'Because java is cool, java is used everywhere. It is quite popular. There are so many libraries available for java',
    100, 0, 'chintan.gm', 1
);

INSERT INTO answers(body, upvotes, downvotes, author, qid) VALUES(
    'You shouldn''t! Use python, it is damn good, smaller and beautiful code',
    10000, 0, 'raj.mm', 1
);

-- followers TABLE

INSERT INTO followers(following_to, followed_by) VALUES('meetmangukiya', 'chintan.gm');
INSERT INTO followers(following_to, followed_by) VALUES('meetmangukiya', 'raj.mm');
INSERT INTO followers(following_to, followed_by) VALUES('meetmangukiya', 'vignesh.vaid');
INSERT INTO followers(following_to, followed_by) VALUES('raj.mm', 'chintan.gm');
INSERT INTO followers(following_to, followed_by) VALUES('raj.mm', 'vignesh.vaid');
INSERT INTO followers(following_to, followed_by) VALUES('vinesh.vaid', 'meetmangukiya');
INSERT INTO followers(following_to, followed_by) VALUES('chintan.gm', 'vignesh.vaid');

-- tags table

INSERT INTO tags(name, description) VALUES(
    'java',
    'java is one of the most popular programming languages.'
);

INSERT INTO tags(name, description) VALUES(
    'angular',
    'angular is one of the most popular frontend framework.'
);

INSERT INTO tags(name, description) VALUES(
    'frontend',
    'frontend is usually what is visible to the users'
);

INSERT INTO tags(name, description) VALUES(
    'backend',
    'backend usually is on the server and where all the data processing is done'
);

-- question_tags table

INSERT INTO question_tags(qid, tag) VALUES(1, 'java');
INSERT INTO question_tags(qid, tag) VALUES(1, 'backend');
INSERT INTO question_tags(qid, tag) VALUES(2, 'angular');
INSERT INTO question_tags(qid, tag) VALUES(2, 'frontend');

-- question_comments table

INSERT INTO question_comments(qid, body, author, upvotes, downvotes) VALUES(
    1, 'this is a comment on question about backend', 'vignesh.vaid', 0, 0
);

-- answer_comments table

INSERT INTO answer_comments(qid, body, answer_author, upvotes, downvotes, author) VALUES(
    1, 'interesting', 'chintan.gm', 0, 0, 'meetmangukiya'
);
