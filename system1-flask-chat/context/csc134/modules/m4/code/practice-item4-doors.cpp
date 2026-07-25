// practice-item4-doors.cpp — M4 Practice exit ticket, Item 4 (predict-output, switch default)
// Single-file, main-only (pre-M6 convention).
// Build: g++ -std=c++17 -Wall -Wextra -o practice-item4-doors practice-item4-doors.cpp
#include <iostream>
using namespace std;

int main()
{
    int door = 3;

    switch (door)
    {
        case 1:
            cout << "Treasure!\n";
            break;
        case 2:
            cout << "A healing fountain.\n";
            break;
        default:
            cout << "You walk into a wall.\n";
    }

    return 0;
}
