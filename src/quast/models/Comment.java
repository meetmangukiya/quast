package quast.models;

import quast.models.User;

/**
 * Comment class representing a comment.
 */
public class Comment {
    protected User author;
    protected int upvote;
    protected int downvotes;
    protected String body;

    /**
     * upvote the comment and update the data in database
     */
    public void upvote() {};

    /**
     * downvote the comment and update the data in database
     */
    public void downvote() {};
}
