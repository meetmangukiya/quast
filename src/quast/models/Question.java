package quast.models;

import java.util.ArrayList;

import quast.models.User;
import quast.models.Answer;

/**
 * Question class representing a question.
 */
public class Question {

    public User author;
    public String title;
    public String body;
    public int upvotes;
    public int downvotes;
    public int qid;

    /**
     * Construct question from qid.
     * @param qid Question ID
     */
    public Question(int qid) {}

    public void upvote() {}

    public void downvote() {}

    /**
     * Get all the answers of given question.
     * @return List of answer objects
     */
    public ArrayList<Answer> answers() {
        ArrayList<Answer> answers = new ArrayList<>();
        return answers;
    }
}