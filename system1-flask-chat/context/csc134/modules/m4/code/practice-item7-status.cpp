// practice-item7-status.cpp — M4 Practice exit ticket, Item 7 (code -> flowchart match)
// The if/else-if/else chain students match to the correct flowchart. Verifies the
// code prints exactly one status line per hp value. Single-file, main-only.
// Build: g++ -std=c++17 -Wall -Wextra -o practice-item7-status practice-item7-status.cpp
#include <iostream>
using namespace std;

int main()
{
    int hp = 0;
    cout << "Enter hp (0-100): ";
    cin >> hp;

    if (hp >= 50)
        cout << "Healthy\n";
    else if (hp >= 20)
        cout << "Wounded\n";
    else
        cout << "Critical\n";

    return 0;
}
