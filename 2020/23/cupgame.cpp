#include <iostream>
#include <list>
#include <vector>

using namespace std;

ostream &operator<<(ostream &os, vector<int> vec) {
    os << "{";
    for (auto elem : vec)
        os << elem << ", ";
    os << "}";
    return os << endl;
}

class Cupgame {
private:
    vector<int> cups;
    int current;
    const int maxlabel;
public:
    Cupgame(const vector<int> &cups_, bool extra=false) : cups(cups_.size()+1), current(cups_[0]), maxlabel(extra? 1000000 : 9) {
        cups[0] = -1;
        /* cout << cups_[0] << " -> "; */
        for (int i = 0; i < 8; i++) {
            cups[cups_[i]] = cups_[i+1];
            /* cout << cups_[i+1] << " -> "; */
        }
        if (extra) {
            cups.reserve(1000000-10);
            cups[cups_[8]] = 10;
            for (int i = 11; i < 1000001; i++)
                cups.emplace_back(i);
            cups.emplace_back(cups_[0]);
            /* cout << cups[cups_[8]] << " -> " << cups[10] */
            /*      << " -> ... -> " << cups[999999] */
            /*      << " -> " << cups[1000000] << endl; */
            /* cout << cups.size() << endl; */
        } else {
            cups[cups_[8]] = cups_[0];
        }
    }

    void move_cups() {
        // Identify cups
        int cup1 = cups[current];
        int cup2 = cups[cup1];
        int cup3 = cups[cup2];
        // Take 'em out
        cups[current] = cups[cup3];
        // Find destination
        int destination = current - 1;
        if (destination < 1) destination = maxlabel;
        while (destination == cup1 || destination == cup2 || destination == cup3)
            destination = (destination - 1 < 1) ? maxlabel : destination - 1;
        // Make the move
        int after = cups[destination];
        cups[destination] = cup1;
        cups[cup3] = after;
        // Select next cup as current
        current = cups[current];
    }

    long thosecups() {
        // Debugged this code for AGES before thinking
        // "maybe it's an integer overflow?"
        return (long)cups[1] * (long)cups[cups[1]];
    }

    friend ostream &operator<<(ostream &os, Cupgame game) {
        int cup = 1;
        do {
            os << cup;
            cup = game.cups[cup];
        } while (cup != 1);
        return os;
    }
};

int main() {
    {
        // Part one
        auto game = Cupgame(vector<int>{2, 1, 9, 7, 4, 8, 3, 6, 5});
        for (int i = 0; i < 100; i++)
            game.move_cups();
        cout << game << endl;
    }
    {
        // Part two
        auto game = Cupgame(vector<int>{2, 1, 9, 7, 4, 8, 3, 6, 5}, true);
        for (int i = 0; i < 10000000; i++)
            game.move_cups();
        cout << game.thosecups() << endl;
    }
}
