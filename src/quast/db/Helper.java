package quast.db;

import java.sql.*;

public class Helper {

    private Connection conn;

    /**
     * Connects to database and stores the connection in conn private variable
     */
    public Helper() {
        this.conn = null;

        String url = "jdbc:postgresql://localhost/" + System.getenv("DB_NAME");
        String user = System.getenv("DB_USER");
        String password = System.getenv("DB_PASS");

        if (url.endsWith("null") || user == null || password == null) {
            System.out.println("ERROR!! Either of the DB_NAME, " +
                               "DB_USER or DB_PASS is not set");
            System.exit(-1);
        }

        try {
            this.conn = DriverManager.getConnection(url, user, password);
        }
        catch (Exception e) {
            System.out.println("Exception: " + e);
            e.printStackTrace();
        }
    }

    /**
     * Use this to execute SQL that'll yield results.
     *
     * @param sql SQL query to be executed.
     * @return ResultSet object containing the result sets.
     */
    public ResultSet retrieve(String sql) throws SQLException {
        ResultSet rs = null;
        Statement st = conn.createStatement();
        rs = st.executeQuery(sql);
        return rs;
    }

    /**
     * Use this to execute SQL that'll not yield any results.
     *
     * @param sql SQL query to be executed.
     * @return Row count or 0 if the statement returns nothing.
     */
    public int update(String sql) throws SQLException {
        Statement st = conn.createStatement();
        return st.executeUpdate(sql);
    }
}
