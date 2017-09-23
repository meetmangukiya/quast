CREATE TABLE users (
    username text,
    bio text DEFAULT '',
    credits int DEFAULT 0,
    PRIMARY KEY (username)
);

CREATE TABLE questions (
    title text,
    description text DEFAULT '',
    author text REFERENCES users(username),
    upvotes int DEFAULT 0,
    downvotes int DEFAULT 0,
    qid SERIAL,
    PRIMARY KEY (qid),
    UNIQUE (title, author)
);

CREATE TABLE answers (
    body text NOT NULL,
    author text REFERENCES users(username),
    qid int REFERENCES questions(qid),
    upvotes int DEFAULT 0,
    downvotes int DEFAULT 0,
    PRIMARY KEY (qid, author),
);

CREATE TABLE tags (
    name text,
    description text DEFAULT '',
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
    body text NOT NULL,
    author text REFERENCES users(username),
    upvotes int DEFAULT 0,
    downvotes int DEFAULT 0,
    PRIMARY KEY (qid, body)
);

CREATE TABLE answer_comments (
    qid int,
    answer_author text,
    FOREIGN  KEY(qid, answer_author) REFERENCES answers(qid, author),
    body text NOT NULL,
    author text REFERENCES users(username),
    upvotes int DEFAULT 0,
    downvotes int DEFAULT 0,
    PRIMARY KEY (qid, answer_author, body)
);
