package quast.models;

import java.sql.SQLException;

import quast.db.Helper;

public class Tag {
    private String name;
    private String description;

    public Tag(String name) {
        name = name;
        Helper db = new Helper();
        try {
            description = db.retrieve(String.format(
                "SELECT description FROM tags WHERE name=%s",
                name)).getString(1);
        }
        catch (SQLException ex) {
            System.out.println("Exception: " + ex);
            ex.printStackTrace();
        }
    }
}
