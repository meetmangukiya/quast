CREATE TABLE users (
    username text,
    bio text,
    PRIMARY KEY (username)
);

CREATE TABLE questions (
    title text,
    description text,
    author text REFERENCES users(username),
    upvotes int,
    downvotes int,
    qid SERIAL,
    PRIMARY KEY (qid)
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
    following_to text REFERENCES users(username)
);

CREATE TABLE question_tags (
    qid int REFERENCES questions(qid),
    tag text REFERENCES tags(name)
);
