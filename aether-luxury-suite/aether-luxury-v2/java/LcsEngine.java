/**
 * Aether LCS — Java reference implementation.
 *
 * Immutable utility class using int[][] for portability across JDK targets.
 */
public final class LcsEngine {

    private LcsEngine() {
        // Utility class.
    }

    public static String lcs(String a, String b) {
        int m = a.length();
        int n = b.length();
        int[][] dp = new int[m + 1][n + 1];

        for (int i = 1; i <= m; i++) {
            char ai = a.charAt(i - 1);
            int[] row = dp[i];
            int[] prev = dp[i - 1];
            for (int j = 1; j <= n; j++) {
                row[j] = ai == b.charAt(j - 1)
                    ? prev[j - 1] + 1
                    : Math.max(prev[j], row[j - 1]);
            }
        }

        int i = m;
        int j = n;
        StringBuilder out = new StringBuilder();
        while (i > 0 && j > 0) {
            if (a.charAt(i - 1) == b.charAt(j - 1)) {
                out.append(a.charAt(i - 1));
                i--;
                j--;
            } else if (dp[i - 1][j] > dp[i][j - 1]) {
                i--;
            } else {
                j--;
            }
        }
        return out.reverse().toString();
    }

    public static void main(String[] args) {
        String[][] cases = {
            {"thisisatest", "testing123testing", "tsitest"},
            {"ABCDGH", "AEDFHR", "ADH"},
            {"AGGTAB", "GXTXAYB", "GTAB"},
            {"BDACDB", "BDCB", "BDCB"},
            {"ABAZDC", "BACBAD", "ABAD"},
        };

        int passed = 0;
        for (String[] c : cases) {
            String result = lcs(c[0], c[1]);
            if (result.equals(c[2])) {
                passed++;
            } else {
                System.err.printf(
                    "FAIL: lcs(%s, %s) -> %s, expected %s%n",
                    c[0], c[1], result, c[2]
                );
            }
        }
        System.out.printf("Java LCS tests: %d/%d passed%n", passed, cases.length);
    }
}
