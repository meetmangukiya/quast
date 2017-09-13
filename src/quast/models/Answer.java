package quast.models;

import java.sql.ResultSet;
import java.sql.SQLException;

import quast.db.Helper;
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
        this.qid = qid;
        this.aid = aid;
        Helper db = new Helper();
        try {
            ResultSet rs = db.retrieve(String.format(
                "SELECT author, body, upvotes, downvotes FROM answers " +
                "WHERE qid=%d AND aid=%d",
                qid, aid
            ));
            rs.next();
            this.author = new User(rs.getString(1));
            this.body = rs.getString(2);
            this.upvotes = rs.getInt(3);
            this.downvotes = rs.getInt(4);
        }
        catch (SQLException ex) {
            System.out.println("Exception: " + ex);
            ex.printStackTrace();
        }
    }

    public void upvote() {}

    public void downvote() {}
}
