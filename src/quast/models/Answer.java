package quast.models;

import quast.models.User;

/**
 * Answer class representing an answer.
 */
public class Answer{
    public User author;
    public String body;
    public int upvotes;
    public int downvotes;
    public int aid;
    public int qid;

    /**
     * @param qid Question ID
     * @param aid Answer ID
     */
    public Answer(int qid, int aid) {}

    public void upvote() {}

    public void downvote() {}
}
