package quast.models;

import quast.models.User;

/**
 * Comment class representing a comment.
 */
public class Comment {
    private User author;
    private int upvote;
    private int downvotes;
    private String body;
    
    /**
     * upvote the comment and update the data in database
     */
    public void upvote() {};
    
    /**
     * downvote the comment and update the data in database
     */
    public void downvote() {};
}
