-- A schema for the joke application
-- Deleting old data
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Joke;
DROP TABLE IF EXISTS Joke_like;
DROP TABLE IF EXISTS Joke_rating;
DROP TABLE IF EXISTS Comment;
DROP TABLE IF EXISTS Comment_like;
DROP TABLE IF EXISTS Reply;
DROP TABLE IF EXISTS Reply_like;
DROP TABLE IF EXISTS Reaction;
DROP TRIGGER IF EXISTS add_joke_like_status;
DROP TRIGGER IF EXISTS add_comment_like_status;
DROP TRIGGER IF EXISTS add_reply_like_status;
DROP TRIGGER IF EXISTS change_joke_like_status;
DROP TRIGGER IF EXISTS change_comment_like_status;
DROP TRIGGER IF EXISTS change_reply_like_status;
DROP TRIGGER IF EXISTS remove_joke_like_status;
DROP TRIGGER IF EXISTS remove_comment_like_status;
DROP TRIGGER IF EXISTS remove_reply_like_status;
DROP TRIGGER IF EXISTS update_rating_on_insert;
DROP TRIGGER IF EXISTS update_rating_on_update;

/* 
 This is User table and it stores the details to the users registered.
 This table has to ensure that the username and email must be unique
 as no two users can be given with the same username or handle and
 no two user accounts can share the same email address. Also, it ensures
 that the email address of the user is already verified.
 */
CREATE TABLE User(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    email_verified INTEGER NOT NULL DEFAULT 0,
    password TEXT NOT NULL
);

/* 
 This is Joke table and stores the usual details to the joke.
 It's likes and dislikes columns are only intended to be updated by
 the triggers defined at the end after an insertion or deletion on Joke_like
 table, and hence should be untouched by the (inserted or updated upon) by
 any other query. Similarly, there is rating column, which is updted by the
 triggers created below, and should not be touched by the any other insert or
 update query.
 */
CREATE TABLE Joke(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    posting_date TIMESTAMP NOT NULL,
    likes INTEGER NOT NULL DEFAULT 0,
    dislikes INTEGER NOT NULL DEFAULT 0,
    rating REAL NOT NULL DEFAULT 0.0,
    poster_id INTEGER NOT NULL REFERENCES User(id)
);

/* 
 This table stores like and dislike status of a particular joke by a
 particular user. The primary key provided for this table ensures that
 the user, should either be able to like or dislike the joke but not both.
 Also, it prevents the user from liking or disliking the same joke multiple
 times
 */
CREATE TABLE Joke_like(
    joke_id INTEGER NOT NULL REFERENCES Joke(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES User(id),
    like_status INTEGER NOT NULL,
    PRIMARY KEY(joke_id, user_id)
);

/* 
 This table stores the rating given by a user on a particular joke. the rating column
 can be any integer between 1 to 5. The primary key ensures that the user can rate a particular
 joke only once.
 */
CREATE TABLE Joke_rating(
    joke_id INTEGER NOT NULL REFERENCES Joke(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES User(id),
    rating INTEGER NOT NULL,
    PRIMARY KEY(joke_id, user_id)
);

/* 
 This table stores comments on different jokes by different users. It also stores
 usual details of the comment, like comment time and commenter id and joke id.
 Here also, the likes and dislikes columns are to be updated only bythe triggers specified
 below and should not be touched by any other query.
 */
CREATE TABLE Comment(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    comment_date TIMESTAMP NOT NULL,
    likes INTEGER NOT NULL DEFAULT 0,
    dislikes INTEGER NOT NULL DEFAULT 0,
    commentor_id INTEGER NOT NULL REFERENCES User(id),
    joke_id INTEGER NOT NULL REFERENCES Joke(id) ON DELETE CASCADE
);

/* 
 This table stores replies of the comments in Comment table. It also has usual likes and dislikes
 which are to be updated by triggers. It also enforces a user to reply a comment only once.
 */
CREATE TABLE Reply(
    comment_id INTEGER NOT NULL REFERENCES Comment(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES User(id),
    content TEXT NOT NULL,
    reply_date TIMESTAMP NOT NULL,
    likes INTEGER NOT NULL DEFAULT 0,
    dislikes INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (comment_id, user_id)
);

/* 
 This table also stores like status of a particular comment by a particular user, just like
 the Joke_like table. Similar to that table, it also enforces the user to like or dislike
 (but not both) a particular comment only once.
 */
CREATE TABLE Comment_like(
    comment_id INTEGER NOT NULL REFERENCES Comment(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES User(id),
    like_status INTEGER NOT NULL,
    PRIMARY KEY(comment_id, user_id)
);
/* 
 This table stores like status of replies in Reply table. It also enforces a particular user
 to like or dislike only once.
 */
 CREATE TABLE Reply_like(
    reply_comment_id INTEGER NOT NULL REFERENCES Reply(comment_id) ON DELETE CASCADE,
    reply_user_id INTEGER NOT NULL REFERENCES Reply(user_id),
    user_id INTEGER NOT NULL REFERENCES User(id),
    like_status INTEGER NOT NULL,
    PRIMARY KEY(reply_comment_id, reply_user_id, user_id)
);

/* 
 This table stores reactions given by different users on different jokes. The reaction_type
 is an integer between 1 to 5 representing 5 different types of reactions allowed in a joke.
 The correct meaning of each number in the reaction_type is specifed by the application's con
 -figurations. Also, the primary key ensures the a user can react to a particular joke only in
 one way.
 */
CREATE TABLE Reaction(
    joke_id INTEGER NOT NULL REFERENCES Joke(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES User(id),
    reaction_type INTEGER NOT NULL,
    PRIMARY KEY(joke_id, user_id) 
);


-- Triggers to update likes and dislikes count for joke and comments and their replies
-- As like_status would be a boolean value 1 means like and 0 means dislike, NOT operator is used as hack to update dislikes
CREATE TRIGGER add_joke_like_status AFTER INSERT ON Joke_like
BEGIN
    UPDATE Joke SET likes = likes + new.like_status, dislikes = dislikes + (NOT new.like_status)
    WHERE id = new.joke_id;
END;
CREATE TRIGGER add_comment_like_status AFTER INSERT ON Comment_like
BEGIN
    UPDATE Comment SET likes = likes + new.like_status, dislikes = dislikes + (NOT new.like_status)
    WHERE id = new.comment_id;
END;
CREATE TRIGGER add_reply_like_status AFTER INSERT ON Reply_like
BEGIN
    UPDATE Reply SET likes = likes + new.like_status, dislikes = dislikes + (NOT new.like_status)
    WHERE comment_id = new.reply_comment_id AND user_id = new.reply_user_id;
END;

CREATE TRIGGER change_joke_like_status AFTER UPDATE ON Joke_like
BEGIN
    UPDATE Joke SET likes = likes - old.like_status, dislikes = dislikes - (NOT old.like_status)
    WHERE id = old.joke_id;
    UPDATE Joke SET likes = likes + new.like_status, dislikes = dislikes + (NOT new.like_status)
    WHERE id = new.joke_id;
END;
CREATE TRIGGER change_comment_like_status AFTER UPDATE ON Comment_like
BEGIN
    UPDATE Comment SET likes = likes - old.like_status, dislikes = dislikes - (NOT old.like_status)
    WHERE id = old.comment_id;
    UPDATE Comment SET likes = likes + new.like_status, dislikes = dislikes + (NOT new.like_status)
    WHERE id = new.comment_id;
END;
CREATE TRIGGER change_reply_like_status AFTER UPDATE ON Reply_like
BEGIN
    UPDATE Reply SET likes = likes - old.like_status, dislikes = dislikes - (NOT old.like_status)
    WHERE comment_id = old.reply_comment_id AND user_id = old.reply_user_id;
    UPDATE Reply SET likes = likes + new.like_status, dislikes = dislikes + (NOT new.like_status)
    WHERE comment_id = new.reply_comment_id AND user_id = new.reply_user_id;
END;

CREATE TRIGGER remove_joke_like_status AFTER DELETE ON Joke_like
BEGIN
    UPDATE Joke SET likes = likes - old.like_status, dislikes = dislikes - (NOT old.like_status)
    WHERE id = old.joke_id;
END;
CREATE TRIGGER remove_comment_like_status AFTER DELETE ON Comment_like
BEGIN 
    UPDATE Comment SET likes = likes - old.like_status, dislikes = dislikes - (NOT old.like_status)
    WHERE id = old.comment_id;
END;
CREATE TRIGGER remove_reply_like_status AFTER DELETE ON Reply_like
BEGIN 
    UPDATE Reply SET likes = likes - old.like_status, dislikes = dislikes - (NOT old.like_status)
    WHERE comment_id = old.reply_comment_id AND user_id = old.reply_user_id;
END;

-- Triggers to update ratings of a joke
CREATE TRIGGER update_rating_on_insert AFTER INSERT ON Joke_rating
BEGIN
    UPDATE Joke SET rating = (SELECT AVG(rating) FROM Joke_rating WHERE id = new.joke_id )
    WHERE id = new.joke_id;
END;
CREATE TRIGGER update_rating_on_update AFTER UPDATE ON Joke_rating
BEGIN
    UPDATE Joke SET rating = (SELECT AVG(rating) FROM Joke_rating WHERE id = new.joke_id )
    WHERE id = new.joke_id;
END;
