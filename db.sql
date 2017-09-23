CREATE TABLE users (
    username text,
    bio text,
    credits int,
    PRIMARY KEY (username)
);

CREATE TABLE questions (
    title text,
    description text,
    author text REFERENCES users(username),
    upvotes int,
    downvotes int,
    qid SERIAL,
    PRIMARY KEY (qid),
    UNIQUE (title, author)
);

CREATE TABLE answers (
    body text,
    author text REFERENCES users(username),
    qid int REFERENCES questions(qid),
    aid int,
    upvotes int,
    downvotes int,
    PRIMARY KEY (qid, aid)
);

CREATE TABLE tags (
    name text,
    description text,
    PRIMARY KEY (name)
);

CREATE TABLE followers (
    followed_by text REFERENCES users(username),
    following_to text REFERENCES users(username),
    PRIMARY KEY (followed_by, following_to)
);

CREATE TABLE question_tags (
    qid int REFERENCES questions(qid),
    tag text REFERENCES tags(name),
    PRIMARY KEY (qid, tag)
);

CREATE TABLE question_comments (
    qid int REFERENCES questions(qid),
    body text,
    author text REFERENCES users(username),
    upvotes int,
    downvotes int,
    PRIMARY KEY (qid, body)
);

CREATE TABLE answer_comments (
    qid int,
    aid int,
    FOREIGN  KEY(qid, aid) REFERENCES answers(qid, aid),
    body text,
    author text REFERENCES users(username),
    upvotes int,
    downvotes int,
    PRIMARY KEY (qid, aid, body)
);
