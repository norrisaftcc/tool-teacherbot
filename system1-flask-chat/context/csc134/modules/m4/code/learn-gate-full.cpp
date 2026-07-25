// learn-gate-full.cpp — M4 Learn, Stage C
// The whole gate in one program: a switch on class, a nested question only
// the Rogue is asked, a compound condition (&&), and an if / else if / else
// chain that decides the outcome. Single pass, no loops, everything in main.
#include <iostream>
using namespace std;

int main()
{
    int characterClass = 0;   // 1 = Warrior, 2 = Mage, 3 = Rogue
    cout << "Your class? (1 = Warrior, 2 = Mage, 3 = Rogue): ";
    cin >> characterClass;

    switch (characterClass)
    {
        case 1:
            cout << "\"A Warrior.\"\n";
            break;
        case 2:
            cout << "\"A Mage.\"\n";
            break;
        case 3:
            cout << "\"A Rogue.\"\n";
            break;
        default:
            cout << "\"I do not know that class. Off you go.\"\n";
            return 0;   // one bad answer ends the visit (single pass)
    }

    int strength = 0;         // a whole number, 0 to 100
    cout << "Your strength score (0-100): ";
    cin >> strength;

    bool hasLockpick = false;
    if (characterClass == 3)          // nested: only a Rogue is asked
    {
        int answer = 0;               // 1 = yes, anything else = no
        cout << "Do you carry a lockpick? (1 = yes, 0 = no): ";
        cin >> answer;
        hasLockpick = (answer == 1);
    }

    if (strength >= 70)
    {
        cout << "The gate swings wide. Go through.\n";
    }
    else if (strength >= 40 && hasLockpick)   // compound: BOTH must be true
    {
        cout << "Not strong, but those clever hands might do.\n";
    }
    else if (strength >= 40)
    {
        cout << "Borderline. Answer my riddle and the gate is yours.\n";
    }
    else
    {
        cout << "Too weak, and no trick to make up for it. Turned away.\n";
    }

    return 0;
}
