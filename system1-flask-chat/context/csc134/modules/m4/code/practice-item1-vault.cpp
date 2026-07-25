// practice-item1-vault.cpp — M4 Practice exit ticket, Item 1 (predict-output)
// Single-file, main-only (pre-M6 convention). No functions, no prototypes.
// Build: g++ -std=c++17 -Wall -Wextra -o practice-item1-vault practice-item1-vault.cpp
#include <iostream>
using namespace std;

int main()
{
    int gold = 45;

    if (gold >= 50)
        cout << "You may enter the treasure vault.\n";
    else
        cout << "Not enough gold. Come back richer.\n";

    return 0;
}
