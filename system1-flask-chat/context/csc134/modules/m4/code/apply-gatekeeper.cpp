// apply-gatekeeper.cpp — CSC-134 M4 (Decisions) Apply-beat tutorial program
//
// The Dungeon Gatekeeper: a single-pass decision program. She reads your
// class with a switch, measures your strength with an if / else-if / else
// ladder, and gives a Rogue with a lockpick a shortcut using a compound
// condition (&&). No loops, no functions — everything lives in main
// (the pre-M6 single-file convention).
//
// This program is built in the Apply tutorial in four stages; each stage
// compiles and runs on its own. The stage markers below match the tutorial.
//
// Build: g++ -std=c++17 -Wall -Wextra -o apply-gatekeeper apply-gatekeeper.cpp

#include <iostream>
using namespace std;

int main()
{
    // ===== STAGE 1: the gatekeeper greets you =====
    cout << "A gatekeeper blocks the dungeon door. She looks you over.\n";

    // ===== STAGE 2: she asks your class (switch) =====
    int characterClass = 0;   // 1 = Warrior, 2 = Mage, 3 = Rogue
    cout << "Your class? (1 = Warrior, 2 = Mage, 3 = Rogue): ";
    cin >> characterClass;

    switch (characterClass)
    {
        case 1:
            cout << "\"A Warrior. Strong arms, I hope.\"\n";
            break;
        case 2:
            cout << "\"A Mage. Let us see if the mind is as sharp as the robes.\"\n";
            break;
        case 3:
            cout << "\"A Rogue. Keep your hands where I can see them.\"\n";
            break;
        default:
            cout << "\"I do not know that class. Off you go.\"\n";
            cout << "The gate stays shut. (Unknown class.)\n";
            return 0;   // single pass — one bad answer ends the visit
    }

    // ===== STAGE 3: she measures your strength (if / else-if / else) =====
    int strength = 0;         // a whole number, 0 to 100
    cout << "Your strength score (0-100): ";
    cin >> strength;

    // ===== STAGE 4: a Rogue may carry a lockpick (compound condition) =====
    bool hasLockpick = false;
    if (characterClass == 3)
    {
        int answer = 0;       // 1 = yes, anything else = no
        cout << "\"A Rogue, hm. Do you carry a lockpick? (1 = yes, 0 = no): \"";
        cin >> answer;
        hasLockpick = (answer == 1);
    }

    // The branching outcome. Highest bar first, then the softer bars.
    if (strength >= 70)
    {
        cout << "The gate swings wide. \"Strong enough. Go through.\"\n";
    }
    else if (strength >= 40 && hasLockpick)
    {
        // A middling Rogue with the right tools earns a shortcut.
        cout << "\"Not strong — but those clever hands might do.\"\n";
        cout << "She looks away. You pick the lock and slip inside.\n";
    }
    else if (strength >= 40)
    {
        cout << "\"Borderline. Answer me this and the gate is yours:\"\n";
        cout << "\"What must be broken before you can use it?\"\n";
        cout << "(Answer it in your head — the gate waits, half-open.)\n";
    }
    else
    {
        cout << "\"Too weak, and no trick to make up for it. Turned away.\"\n";
    }

    cout << "The visit ends.\n";
    return 0;
}
