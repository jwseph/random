#include <bits/stdc++.h>
using namespace std;

#define NONE 0
#define FIRST 1
#define SECOND 2

struct Board {
    static const int nr = 6, nc = 7;
    vector<vector<int>> grid = vector<vector<int>>(nr, vector<int>(nc));
    friend ostream& operator << (ostream& os, const Board& b) {
        cout << string(13, '-') << endl;
        for (int r = 0; r < 6; ++r) {
            for (int c = 0; c < 7; ++c) {
                int val = b.grid[r][c];
                cout << (val == NONE ? ' ' : val == FIRST ? 'O' : val == SECOND ? 'X' : '?')  << ' ';
            }
            cout << endl;
        }
        cout << string(13, '-') << endl;
        return os;
    }
    int won() {
        // columns
        for (int c = 0; c < nc; ++c) {
            int cur = NONE, cnt = 0;
            for (int r = 0; r < nr; ++r) {
                if (grid[r][c] == NONE || grid[r][c] != cur) {
                    cur = grid[r][c];
                    cnt = 1;
                }
                if (cnt == 4) return cur;
            }
        }
        // rows
        for (int r = 0; r < nr; ++r) {
            int cur = NONE, cnt = 0;
            for (int c = 0; c < nc; ++c) {
                if (grid[r][c] == NONE || grid[r][c] != cur) {
                    cur = grid[r][c];
                    cnt = 1;
                }
                if (cnt == 4) return cur;
            }
        }
        // diags - northeast
        for (int i = 0; i <= nr+nc-2; ++i) {
            int cur = NONE, cnt = 0;
            for (int c = 0; c <= i; ++c) {
                int r = i-c;
                if (r >= nr || c >= nc) continue;
                if (grid[r][c] == NONE || grid[r][c] != cur) {
                    cur = grid[r][c];
                    cnt = 1;
                }
                if (cnt == 4) return cur;
            }
        }
        // diags - southeast
        for (int i = 0; i <= nr+nc-2; ++i) {
            int cur = NONE, cnt = 0;
            for (int c = 0; c <= i; ++c) {
                int r = i-c;
                if (r >= nr || c >= nc) continue;
                r = nr-1-r;
                if (grid[r][c] == NONE || grid[r][c] != cur) {
                    cur = grid[r][c];
                    cnt = 1;
                }
                if (cnt == 4) return cur;
            }
        }
        return NONE;
    }
};

int main() {
  cout << "Hello world" << endl;
  Board b;
  cout << b;
}