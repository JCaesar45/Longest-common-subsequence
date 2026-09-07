import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class LcsEngineTest {

    @Test
    public void testRosettaCases() {
        assertEquals("tsitest", LcsEngine.lcs("thisisatest", "testing123testing"));
        assertEquals("ADH", LcsEngine.lcs("ABCDGH", "AEDFHR"));
        assertEquals("GTAB", LcsEngine.lcs("AGGTAB", "GXTXAYB"));
        assertEquals("BDCB", LcsEngine.lcs("BDACDB", "BDCB"));
        assertEquals("ABAD", LcsEngine.lcs("ABAZDC", "BACBAD"));
    }

    @Test
    public void testCaseSensitivity() {
        assertEquals("", LcsEngine.lcs("ABC", "abc"));
    }

    @Test
    public void testEmptyInputs() {
        assertEquals("", LcsEngine.lcs("", "anything"));
        assertEquals("", LcsEngine.lcs("anything", ""));
    }
}
