package quast.models;

import java.sql.ResultSet;
import java.sql.SQLException;

import quast.db.Helper;

/**
 * Class representing a User
 */
public class User {
    private String username;
    private String bio;
    private int credits;

    /**
     * Construct User object from username.
     * @param username
     */
    public User(String username) {
        this.username = username;
        Helper db = new Helper();
        try {
            ResultSet rs = db.retrieve(String.format(
                            "SELECT credits, bio FROM users WHERE username='%s'",
                            this.username));
            rs.next();
            this.credits = rs.getInt(1);
            this.bio = rs.getString(2);
        }
        catch (SQLException ex) {
            System.out.println("Exception: " + ex);
            ex.printStackTrace();
        }
    }

    @Override
    public String toString() {
        return this.username;
    }
}
