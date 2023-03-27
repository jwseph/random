public class TicTacToe {
    public static void main(String[] args) {
        long t = System.currentTimeMillis();
        System.out.println(sol(0b000000000, 0b000000000, -1, 1, 9));
        System.out.println(System.currentTimeMillis()-t);
    }
    private static int[][] win = new int[][]{
        {0b000000111, 0b001001001, 0b100010001},
        {0b000000111, 0b010010010},
        {0b000000111, 0b100100100, 0b001010100},
        {0b000111000, 0b001001001},
        {0b000111000, 0b010010010, 0b100010001, 0b001010100},
        {0b000111000, 0b100100100},
        {0b111000000, 0b001001001, 0b001010100},
        {0b111000000, 0b010010010},
        {0b111000000, 0b100100100, 0b100010001},
        {},
    };
    private static int sol(int a, int b, int m, int M, int l) {
        for (int s: win[l]) {
            if ((b&s) == s) return -1;
        }
        if ((a|b) == 0b111111111) return 0;
        int r = -2;
        for (int i = 0; i < 9 && m < M; i++) {
            if (((a|b)&1<<i) != 0) continue;
            int s = -sol(b, a|1<<i, -M, -m, i);
            if (r < s) r = s;
            if (m < r) m = r;
        }
        return r;
    }
}
