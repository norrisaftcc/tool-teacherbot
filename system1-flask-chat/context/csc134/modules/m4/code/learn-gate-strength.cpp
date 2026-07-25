// learn-gate-strength.cpp — M4 Learn, Stage A
// The gatekeeper measures your strength. An if / else if / else chain,
// three branches. Comparison operators only, no logic operators yet.
#include <iostream>
using namespace std;

int main()
{
    int strength = 0;                 // a whole number, 0 to 100
    cout << "Your strength score (0-100): ";
    cin >> strength;

    if (strength >= 70)
    {
        cout << "The gate swings wide. Go through.\n";
    }
    else if (strength >= 40)
    {
        cout << "Borderline. Answer my riddle and the gate is yours.\n";
    }
    else
    {
        cout << "Too weak. Turned away.\n";
    }

    return 0;
}
