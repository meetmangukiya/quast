-- Store user details
CREATE TABLE users (
    username text,
    bio text DEFAULT '',
    credits int DEFAULT 0,
    password_hash bytea NOT NULL,
    PRIMARY KEY (username)
);

-- Store follower details
CREATE TABLE followers (
    followed_by text REFERENCES users(username),
    following_to text REFERENCES users(username),
    PRIMARY KEY (followed_by, following_to)
);

-- Store question details
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

-- Store users that upvoted a given question
CREATE TABLE question_upvotes (
    qid int REFERENCES questions(qid),
    username text REFERENCES users(username)
);

-- Store users that downvoted a question
CREATE TABLE question_downvotes (
    qid int REFERENCES questions(qid),
    username text REFERENCES users(username)
);

-- Store answer details
CREATE TABLE answers (
    body text NOT NULL,
    author text REFERENCES users(username),
    qid int REFERENCES questions(qid),
    upvotes int DEFAULT 0,
    downvotes int DEFAULT 0,
    PRIMARY KEY (qid, author)
);

-- Store users that upvoted an answer
CREATE TABLE answer_upvotes (
    qid int REFERENCES questions(qid),
    answer_author text REFERENCES users(username),
    username text REFERENCES users(username)
);

-- Store users that downvoted an answer
CREATE TABLE answer_downvotes (
    qid int REFERENCES questions(qid),
    answer_author text REFERENCES users(username),
    username text REFERENCES users(username)
);

-- Store tags and tag details
CREATE TABLE tags (
    name text,
    description text DEFAULT '',
    PRIMARY KEY (name)
);

-- Store tags added to given question
CREATE TABLE question_tags (
    qid int REFERENCES questions(qid),
    tag text REFERENCES tags(name),
    PRIMARY KEY (qid, tag)
);

-- Store comments of a given question
CREATE TABLE question_comments (
    qid int REFERENCES questions(qid),
    body text NOT NULL,
    author text REFERENCES users(username),
    upvotes int DEFAULT 0,
    downvotes int DEFAULT 0,
    PRIMARY KEY (qid, body)
);

-- Store comments of a given answer
CREATE TABLE answer_comments (
    qid int,
    answer_author text,
    FOREIGN  KEY(qid, answer_author) REFERENCES answers(qid, author),
    body text NOT NULL,
    author text REFERENCES users(username),
    upvotes int DEFAULT 0,
    downvotes int DEFAULT 0,
    PRIMARY KEY (qid, answer_author, author, body)
);

-- Salts table
CREATE TABLE salts (
    salt bytea NOT NULL,
    username text REFERENCES users(username)
);
