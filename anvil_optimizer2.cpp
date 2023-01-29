// Credit to Cal Henderson for original algorithm
// Github: https://github.com/iamcal/enchant-order

#include <bits/stdc++.h>
using namespace std;

typedef int multiplier_t;
typedef int max_level_t;
typedef tuple<max_level_t, multiplier_t, multiplier_t> enchant_data_t;

unordered_map<string, enchant_data_t> enchant_data = {
    {"item", {0, 0, 0}},
    {"protection", {4, 1, 1}},
    {"fire_protection", {4, 2, 1}},
    {"feather_falling", {4, 2, 1}},
    {"blast_protection", {4, 4, 2}},
    {"projectile_protection", {4, 2, 1}},
    {"thorns", {3, 8, 4}},
    {"respiration", {3, 4, 2}},
    {"depth_strider", {3, 4, 2}},
    {"aqua_affinity", {1, 4, 2}},
    {"sharpness", {5, 1, 1}},
    {"smite", {5, 2, 1}},
    {"bane_of_arthropods", {5, 2, 1}},
    {"knockback", {2, 2, 1}},
    {"fire_aspect", {2, 4, 2}},
    {"looting", {3, 4, 2}},
    {"efficiency", {5, 1, 1}},
    {"silk_touch", {1, 8, 4}},
    {"unbreaking", {3, 2, 1}},
    {"fortune", {3, 4, 2}},
    {"power", {5, 1, 1}},
    {"punch", {2, 4, 2}},
    {"flame", {1, 4, 2}},
    {"infinity", {1, 8, 4}},
    {"luck_of_the_sea", {3, 4, 2}},
    {"lure", {3, 4, 2}},
    {"frost_walker", {2, 4, 2}},
    {"mending", {1, 4, 2}},
    {"curse_of_binding", {1, 8, 4}},
    {"curse_of_vanishing", {1, 8, 4}},
    {"impaling", {5, 4, 2}},
    {"riptide", {3, 4, 2}},
    {"loyalty", {3, 1, 1}},
    {"channeling", {1, 8, 4}},
    {"multishot", {1, 4, 2}},
    {"piercing", {4, 1, 1}},
    {"quick_charge", {3, 2, 1}},
    {"soul_speed", {3, 8, 4}},
    {"swift_sneak", {3, 8, 4}},
    {"sweeping_edge", {3, 4, 2}},
};

struct Path {
    int cost;
    int max_cost;
    set<int> remaining;
    vector<pair<int, int>> steps;
    unordered_map<int, int> workings;
    Path() {
        cost = max_cost = 0;
    }
};

string make_key(set<int>& remaining) {
    ostringstream os;
    for (const int& item: remaining) os << item << ' ';
    return os.str();
}

queue<Path*> explode_path(Path* path, unordered_map<int, int>& costs);
int get_item_cost(int item, unordered_map<int, int>& costs);


int solve(map<string, int>& raw_items) {
    unordered_map<int, tuple<string, int, int, int>> enchants;  // tuple is enchant, level, weight, score
    unordered_map<int, int> costs;
    int i = 0;
    set<int> items;
    for (auto it = raw_items.begin(); it != raw_items.end(); ++it) {
        int weight = get<2>(enchant_data[it->first]);
        int cost = weight*it->second;
        enchants[1<<i] = {
            it->first,
            it->second,
            weight,
            cost,
        };
        costs[i] = cost;
        items.insert(1<<i);
        ++i;
    }

    Path* initial_path = new Path;
    initial_path->remaining = items;
    for (const int& item: items) initial_path->workings[item] = 0;
    queue<Path*> incomplete_paths;
    incomplete_paths.push(initial_path);

    Path* best_path = new Path;
    best_path->cost = best_path->max_cost = INT_MAX;
    
    queue<Path*> complete_paths;
    while (!incomplete_paths.empty()) {
        for (int n = incomplete_paths.size(); n > 0; --n) {
            for (queue<Path*> paths = explode_path(incomplete_paths.front(), costs); !paths.empty(); paths.pop()) {
                Path*& path = paths.front();
                if (path->remaining.size() > 1) {  // Will be true until last time this loop occurs
                    incomplete_paths.push(path);
                    continue;
                }
                complete_paths.push(path);
                if (path->cost < best_path->cost || path->cost == best_path->cost && path->max_cost < best_path->max_cost) {
                    best_path = path;
                }
            }
            delete incomplete_paths.front();
            incomplete_paths.pop();
        }
    }

    int best_cost = best_path->cost;
    while (!complete_paths.empty()) {
        delete complete_paths.front();
        complete_paths.pop();
    }

    return best_cost;
}


queue<Path*> explode_path(Path* path, unordered_map<int, int>& costs) {
    unordered_map<string, Path*> best_paths;
    for (auto i = path->remaining.begin(); i != path->remaining.end(); ++i) {
        for (auto j = path->remaining.begin(); j != path->remaining.end(); ++j) {
            if (i == j || *j&1) continue;
            Path* new_path = new Path;
            for (auto k = path->remaining.begin(); k != path->remaining.end(); ++k) {
                if (k == i || k == j) continue;
                new_path->remaining.insert(*k);
            }
            new_path->cost = path->cost;
            new_path->max_cost = path->max_cost;
            new_path->steps = path->steps;
            new_path->workings = path->workings;

            assert(!(*i&*j));  // There should be no intersection in the items
            int c = *i|*j;  // Combined
            new_path->remaining.insert(c);
            
            int work_i = path->workings[*i], work_j = path->workings[*j];
            int work_c = max(work_i, work_j)+1;
            new_path->workings[c] = work_c;
            
            new_path->steps.push_back({*i, *j});
            
            // Calculate step cost
            int step_penalty_cost = (1<<work_i)+(1<<work_j)-2;
            int step_enchant_cost = get_item_cost(*j, costs);
            int step_cost = step_penalty_cost+step_enchant_cost;
            new_path->cost += step_cost;
            new_path->max_cost = max(new_path->max_cost, step_cost);
            
            string key = make_key(new_path->remaining);
            if (best_paths.find(key) != best_paths.end()) {
                Path*& best_path = best_paths[key];
                if (new_path->cost < best_path->cost || new_path->cost == best_path->cost && new_path->max_cost < best_path->max_cost) {
                    delete best_path;
                    best_path = new_path;
                }
            } else {
                best_paths[key] = new_path;
            }
        }
    }

    queue<Path*> paths;
    for (const auto& best_path: best_paths) {
        paths.push(best_path.second);
    }
    return paths;
}


int get_item_cost(int item, unordered_map<int, int>& costs) {
    int total_cost = 0;
    for (int i = 0; item > 0; ++i) {
        if (item&1 && i != 0) total_cost += costs[i];
        item >>= 1;
    }
    return total_cost;
}


int main() {
    map<string, int> items = {
        // {"!tool", -1},
        // {"protection", 4},
        // {"feather_falling", 4},
        // {"depth_strider", 3},
        // {"unbreaking", 3},
        // {"mending", 1},
        // {"thorns", 3},
        {"!tool", -1},
        {"protection", 4},
        {"depth_strider", 3},
        {"feather_falling", 4},
        {"mending", 1},
        {"soul_speed", 3},
        {"thorns", 3},
        {"unbreaking", 3},
    };
    cout << "Starting" << endl;
    chrono::steady_clock::time_point begin = chrono::steady_clock::now();
    cout << solve(items) << endl;
    chrono::steady_clock::time_point end = chrono::steady_clock::now();
    cout << "Time taken: " << chrono::duration_cast<chrono::microseconds>(end-begin).count()/1000000. << " seconds";
}