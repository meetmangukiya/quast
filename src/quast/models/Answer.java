package quast.models;

import java.sql.ResultSet;
import java.sql.SQLException;

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
    public Answer(int qid, int aid) {
        qid = qid;
        aid = aid;
        Helper db = new Helper();
        try {
            ResultSet rs = db.retrieve(String.format(
                "SELECT author, body, upvotes, downvotes FROM answers" +
                "WHERE qid=%d AND aid=%d"
                ),
                qid, aid
            );
            author = rs.getString(1);
            body = rs.getString(2);
            upvotes = rs.getInt(3);
            downvotes = rs.getInt(4);
        }
        catch (SQLException ex) {
            System.out.println("Exception: " + ex);
            ex.printStackTrace();
        }
    }

    public void upvote() {}

    public void downvote() {}
}
