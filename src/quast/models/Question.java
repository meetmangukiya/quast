package quast.models;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;

import quast.db.Helper;
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
    public Question(int qid) {
        this.qid = qid;
        Helper db = new Helper();
        try {
            ResultSet rs = db.retrieve(String.format(
                "SELECT author, title, body, upvotes, downvotes " +
                "FROM questions WHERE question=%d",
                qid));
            this.author = new User(rs.getString(1));
            this.title = rs.getString(2);
            this.body = rs.getString(3);
            this.upvotes = rs.getInt(4);
            this.downvotes = rs.getInt(5);
        }
        catch (SQLException ex) {
            System.out.println("Exception: " + ex);
            ex.printStackTrace();
        }
    }

    /**
     * Create a new question.
     */
    public Question(String title, String description, User author) {
        try {
            this.title = title;
            this.body = description;
            this.author = author;
            this.upvotes = this.downvotes = 0;

            Helper db = new Helper();

            int status = db.update(
                String.format("INSERT INTO questions (title, description, " +
                    "author) VALUES (" +
                    "'%s', '%s', '%s')",
                    title, description, author)
            );

            ResultSet rs = db.retrieve(
                String.format("SELECT qid FROM questions WHERE title='%s' AND " +
                    "author='%s'",
                    title, author)
            );
            rs.next();
            this.qid = rs.getInt(1);
        }
        catch(SQLException ex) {
            System.out.println("Exception: " + ex);
            ex.printStackTrace();
        }
    }

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
