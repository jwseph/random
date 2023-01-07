#include <bits/stdc++.h>
#include <iostream>
using namespace std;

typedef string enchant_name_t;
typedef int multiplier_t;
typedef int max_level_t;
typedef tuple<max_level_t, multiplier_t, multiplier_t> enchant_data_t;
typedef int enchant_index_t;

unordered_map<enchant_name_t, enchant_index_t> enchant_indices = {
    {"protection", 0},
    {"fire_protection", 1},
    {"feather_falling", 2},
    {"blast_protection", 3},
    {"projectile_protection", 4},
    {"thorns", 5},
    {"respiration", 6},
    {"depth_strider", 7},
    {"aqua_affinity", 8},
    {"sharpness", 9},
    {"smite", 10},
    {"bane_of_arthropods", 11},
    {"knockback", 12},
    {"fire_aspect", 13},
    {"looting", 14},
    {"efficiency", 15},
    {"silk_touch", 16},
    {"unbreaking", 17},
    {"fortune", 18},
    {"power", 19},
    {"punch", 20},
    {"flame", 21},
    {"infinity", 22},
    {"luck_of_the_sea", 23},
    {"lure", 24},
    {"frost_walker", 25},
    {"mending", 26},
    {"curse_of_binding", 27},
    {"curse_of_vanishing", 28},
    {"impaling", 29},
    {"riptide", 30},
    {"loyalty", 31},
    {"channeling", 32},
    {"multishot", 33},
    {"piercing", 34},
    {"quick_charge", 35},
    {"soul_speed", 36},
    {"swift_sneak", 37},
    {"sweeping_edge", 38},
};

vector<enchant_data_t> enchant_data = {
    {4, 1, 1},
    {4, 2, 1},
    {4, 2, 1},
    {4, 4, 2},
    {4, 2, 1},
    {3, 8, 4},
    {3, 4, 2},
    {3, 4, 2},
    {1, 4, 2},
    {5, 1, 1},
    {5, 2, 1},
    {5, 2, 1},
    {2, 2, 1},
    {2, 4, 2},
    {3, 4, 2},
    {5, 1, 1},
    {1, 8, 4},
    {3, 2, 1},
    {3, 4, 2},
    {5, 1, 1},
    {2, 4, 2},
    {1, 4, 2},
    {1, 8, 4},
    {3, 4, 2},
    {3, 4, 2},
    {2, 4, 2},
    {1, 4, 2},
    {1, 8, 4},
    {1, 8, 4},
    {5, 4, 2},
    {3, 4, 2},
    {3, 1, 1},
    {1, 8, 4},
    {1, 4, 2},
    {4, 1, 1},
    {3, 2, 1},
    {3, 8, 4},
    {3, 8, 4},
    {3, 4, 2},
};

struct Enchantable {
    int use_count;
    unordered_map<enchant_index_t, int> enchants;
    bool is_tool;
};
int solve(vector<Enchantable*> es, const int max_cost = INT_MAX) {
    if (es.size() <= 1) return 0;
    if (max_cost < 0) return max_cost;
    int min_cost = max_cost;
    for (int i = 0; i < es.size(); ++i) {
        for (int j = 0; j < es.size(); ++j) {
            Enchantable* t = es[i], *s = es[j];
            if (i == j || s->is_tool) continue;
            // combine
            Enchantable* p = new Enchantable;
            p->use_count = max(t->use_count, s->use_count)+1;
            p->is_tool = t->is_tool || s->is_tool;
            p->enchants = t->enchants;
            int cost = (1<<t->use_count)-1 + (1<<s->use_count)-1;  // penalties
            for (const auto& enchant_pair: s->enchants) {
                enchant_index_t ei = enchant_pair.first;
                int s_level = enchant_pair.second;
                int t_level = t->enchants.find(ei) != t->enchants.end() ? t->enchants[ei] : 0;
                int p_level = t_level == s_level ? min(t_level+1, get<0>(enchant_data[ei])) : max(t_level, s_level);
                p->enchants[ei] = p_level;
                cost += p_level*get<2>(enchant_data[ei]);
            }
            // end combine
            int l = i, r = j;
            if (l > r) swap(l, r);
            Enchantable* left = es[l], *right = es[r];
            es[l] = p;
            es[r] = es.back();
            es.pop_back();
            cost += solve(es, min_cost-cost);
            es.push_back(right);
            swap(es[r], es.back());
            es[l] = left;
            min_cost = min(min_cost, cost);
            delete p;
        }
    }
    return min_cost;
}

Enchantable* make_enchantable(unordered_map<enchant_index_t, int> enchants, bool tool = false) {
    Enchantable* res = new Enchantable;
    res->use_count = 0;
    res->is_tool = tool;
    res->enchants = enchants;
    return res;
}

int main() {
    vector<pair<enchant_name_t, enchant_index_t>> stuff = {
        {"protection", 4},
        {"feather_falling", 4},
        {"depth_strider", 3},
        {"unbreaking", 3},
        {"mending", 1},
        {"thorns", 3},
    };
    vector<Enchantable*> things = {make_enchantable({}, true)};
    for (auto& stuf: stuff) {
        things.push_back(make_enchantable({{enchant_indices[stuf.first], stuf.second}}));
    }
    cout << "Starting" << endl;
    chrono::steady_clock::time_point begin = chrono::steady_clock::now();
    cout << solve(things) << endl;
    chrono::steady_clock::time_point end = chrono::steady_clock::now();
    cout << "Time taken: " << chrono::duration_cast<chrono::microseconds>(end-begin).count()/1000000. << " seconds";
    for (Enchantable*& thing: things) {
        delete thing;
    }
}