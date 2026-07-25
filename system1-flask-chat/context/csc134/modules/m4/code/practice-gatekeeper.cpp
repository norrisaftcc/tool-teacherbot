// practice-gatekeeper.cpp — M4 Practice exit ticket shared program (Items 2, 3, 6)
// A trimmed Dungeon Gatekeeper: switch on class, if/else-if/else on strength,
// one compound condition (&&) for a Rogue's lockpick. Same shape as the module's
// canonical decision program. Single-file, main-only (pre-M6 convention).
// Build: g++ -std=c++17 -Wall -Wextra -o practice-gatekeeper practice-gatekeeper.cpp
#include <iostream>
using namespace std;

int main()
{
    int characterClass = 0;   // 1 = Warrior, 2 = Mage, 3 = Rogue
    cout << "Class? (1=Warrior, 2=Mage, 3=Rogue): ";
    cin >> characterClass;

    switch (characterClass)
    {
        case 1:
            cout << "A Warrior steps up.\n";
            break;
        case 2:
            cout << "A Mage steps up.\n";
            break;
        case 3:
            cout << "A Rogue steps up.\n";
            break;
        default:
            cout << "Unknown class. The gate stays shut.\n";
            return 0;
    }

    int strength = 0;         // a whole number, 0 to 100
    cout << "Strength (0-100): ";
    cin >> strength;

    bool hasLockpick = false;
    if (characterClass == 3)
    {
        int answer = 0;       // 1 = yes, anything else = no
        cout << "Lockpick? (1=yes, 0=no): ";
        cin >> answer;
        hasLockpick = (answer == 1);
    }

    if (strength >= 70)
    {
        cout << "The gate swings wide. Go through.\n";
    }
    else if (strength >= 40 && hasLockpick)
    {
        cout << "Clever hands will do. You slip inside.\n";
    }
    else if (strength >= 40)
    {
        cout << "Borderline. Answer the riddle to pass.\n";
    }
    else
    {
        cout << "Too weak. Turned away.\n";
    }

    return 0;
}
