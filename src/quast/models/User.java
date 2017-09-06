package quast.models;

/**
 * Class representing a User
 */
public class User {
    private String username;
    private int credits;
    
    /**
     * Construct User object from username.
     * @param username
     */
    public User(String username) {}

    @Override
    public String toString() {
        return this.username;
    }
}
