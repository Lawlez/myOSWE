package lab.actions.common.serializable;
import java.io.Serializable;

public class AdminPrefs implements Serializable {
    private static final long serialVersionUID = -1270328626346089834L;
// Serial version UID for serialization compatibility
    public String favoriteFood;
    public String favoriteQuote;
    public String favouriteBook;
    public Object theme;
}