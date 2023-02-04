#include <bits/stdc++.h>
using namespace std;

#define EMPTY 0
#define FIRST 1
#define SECOND 2
#define GET_GRID(r, c) (5-(r)+6*(c))

struct Board {
  int grid[42] = {};
  friend ostream& operator <<(ostream& os, const Board& b);
  int won() {
    // columns
    for (int c = 0; c < 7; ++c) {
      for (int sr = 0; sr < 3; ++sr) {
        int val = grid[GET_GRID(sr, c)];
        if (val == EMPTY) continue;
        for (int r = sr+1; r < sr+4; ++r) {
          if (grid[GET_GRID(r, c)] != val) {
            val = EMPTY;
            break;
          }
        }
        if (val == EMPTY) continue;
        return val;
      }
    }
    // rows
    for (int r = 0; r < 6; ++r) {
      for (int sc = 0; sc < 4; ++sc) {
        int val = grid[GET_GRID(r, sc)];
        if (val == EMPTY) continue;
        for (int c = sc+1; c < sc+4; ++c) {
          if (grid[GET_GRID(r, c)] != val) {
            val = EMPTY;
            break;
          }
        }
        if (val == EMPTY) continue;
        return val;
      }
    }
    // bottom-left to top-right diagonals
    for (int r = 0; r < 6; ++r) {
      for (int sc = 0; sc < 4; ++sc) {
        int val = grid[GET_GRID(r, sc)];
        if (val == EMPTY) continue;
        for (int c = sc+1; c < sc+4; ++c) {
          if (grid[GET_GRID(r, c)] != val) {
            val = EMPTY;
            break;
          }
        }
        if (val == EMPTY) continue;
        return val;
      }
    }
  }
};
ostream& operator <<(ostream& os, const Board& b) {
  cout << string(13, '-') << endl;
  for (int r = 0; r < 6; ++r) {
    for (int c = 0; c < 7; ++c) {
      int val = b.grid[GET_GRID(r, c)];
      cout << (val == EMPTY ? ' ' : val == FIRST ? 'O' : val == SECOND ? 'X' : '?')  << ' ';
    }
    cout << endl;
  }
  cout << string(13, '-') << endl;
  return os;
}

int main() {
  cout << "Hello world" << endl;
  Board b;
  cout << b;
}