// learn-gate-class.cpp — M4 Learn, Stage B
// The gatekeeper asks your class. A switch statement, one case per class,
// with a default for anything she does not recognize.
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
            cout << "\"A Warrior. Strong arms, I hope.\"\n";
            break;
        case 2:
            cout << "\"A Mage. A sharp mind, I hope.\"\n";
            break;
        case 3:
            cout << "\"A Rogue. Hands where I can see them.\"\n";
            break;
        default:
            cout << "\"I do not know that class. Off you go.\"\n";
    }

    return 0;
}
