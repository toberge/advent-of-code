#include <unordered_map>
#include <vector>
#include <iostream>

using namespace std;

int n = 10;

/**
 * I did not finish this implementation at all.
 */

vector<pair<int, vector<string>>> read_input() {
    vector<pair<int, vector<string>>> vec;
    int i = 0;
    string line;
    int mode = 0;
    while (cin >> line) {
        if (line == "Tile") {
            if (mode != 0) i++;
            mode = 1;
            continue;
        } else if (mode == 1) {
            auto slice = line.substr(0, 4);
            vec.emplace_back(pair<int, vector<string>>(stoi(slice), vector<string>()));
            mode = 2;
        } else if (mode == 2) {
            vec[i].second.emplace_back(line);
        }
    }
    return vec;
}

unordered_map<int, vector<string>> possible_edges(vector<pair<int, vector<string>>> tiles) {
    unordered_map<int, vector<string>> edges(tiles.size());
    for (auto [id, tile] : tiles) {
        edges.emplace(id, tile[0]);
        edges.emplace(id, tile[n-1]);
        string l, r;
        l.reserve(n);
        r.reserve(n);
        for (int i = 0; i < n; i++) {
            l[i] = tile[i][0];
            r[i] = tile[i][0];
        }
    }
    return edges;
}

/* unordered_map<int, vector<int>> probable_fuckig_edges */

vector<int> find_borders(unordered_map<int, vector<string>> edges) {
    vector<int> borders;
    borders.reserve(4);
    for (auto [id, these_edges] : edges)
        if (these_edges.size() == 2)
            borders.emplace_back(id);
    return borders;
}

int main() {
    const auto pieces = read_input();

    for (auto el : pieces) {
        cout << "Tile: " << el.first << endl;
        for (auto line : el.second) {
            cout << line << endl;
        }
        cout << endl;
    }

    auto borders = find_borders(possible_edges(pieces));
    int prod = 1;
    for (auto id : borders)
        prod *= id;
    cout << prod << endl;
}
