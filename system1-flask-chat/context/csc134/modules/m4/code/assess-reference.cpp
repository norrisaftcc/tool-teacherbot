// assess-reference.cpp — CSC-134 M4 (Decisions) ASSESS-beat reference solution
//
// ============================================================================
// INSTRUCTOR-FACING. NOT part of the student handout. Do NOT distribute this
// file to students. It is the grader's A-tier exemplar for assess-lab.md.
// ============================================================================
//
// This shows the full structure a from-spec student program should reach at the
// top tier: a switch on a class-like input, an if / else-if / else chain (3+
// branches) on a numeric threshold, a compound condition (&&), a genuinely
// nested condition, a single-pass validation rejection (NO loop), and 4+
// distinct endings.
//
// It is a RE-SKIN of the frozen _contracts/m4_gatekeeper.cpp shape (a river
// ferryman instead of a dungeon gatekeeper) to prove the theme strips cleanly
// without touching the decision structure. It deliberately does NOT reuse the
// gatekeeper scene students type in during the Apply tutorial — grading against
// a copy of the Apply program would teach nothing.
//
// M4 machinery ONLY: if / else if / else, switch, comparison + logical
// operators, nested conditions. No loops. No functions or prototypes —
// everything lives in main (the pre-M6 single-file convention).
//
// Built in stages; each stage compiles and runs on its own.
//
// Build: g++ -std=c++17 -Wall -Wextra -o assess-reference assess-reference.cpp

#include <iostream>
using namespace std;

int main()
{
    // ===== STAGE 1: the scene opens =====
    cout << "A ferryman waits at the river's edge. He eyes you.\n";

    // ===== STAGE 2: a switch on a class-like input =====
    int travelerType = 0;   // 1 = Merchant, 2 = Pilgrim, 3 = Smuggler
    cout << "Your trade? (1 = Merchant, 2 = Pilgrim, 3 = Smuggler): ";
    cin >> travelerType;

    switch (travelerType)
    {
        case 1:
            cout << "\"A Merchant. Coin talks loudest here.\"\n";
            break;
        case 2:
            cout << "\"A Pilgrim. The far shore is holy ground.\"\n";
            break;
        case 3:
            cout << "\"A Smuggler. Keep your crates covered.\"\n";
            break;
        default:
            // Designed default ending — a bad class ends the visit, no crash.
            cout << "\"I do not ferry your kind. Away with you.\"\n";
            return 0;
    }

    // ===== STAGE 3: read a numeric threshold input =====
    int coins = 0;          // a whole number, 0 to 100
    cout << "How many coins can you spare? (0-100): ";
    cin >> coins;

    // Single-pass validation (B-tier move): reject out-of-range, then stop.
    // This is ONE check, not a loop-until-valid. Loops arrive in M5.
    if (coins < 0 || coins > 100)
    {
        cout << "\"That is no honest purse. I'll not carry a liar.\"\n";
        return 0;
    }

    // ===== STAGE 4: a Smuggler may flash a bribe token (compound setup) =====
    bool hasToken = false;
    if (travelerType == 3)
    {
        int flash = 0;      // 1 = yes, anything else = no
        cout << "\"A token for the harbor master? (1 = yes, 0 = no): \"";
        cin >> flash;
        hasToken = (flash == 1);
    }

    // ===== STAGE 5: the branching outcome (if / else if / else) =====
    // Highest bar first, then the softer bars.
    if (coins >= 70)
    {
        cout << "\"Full fare. Step aboard.\"\n";
        // A genuinely nested condition inside the top branch.
        if (travelerType == 2)
        {
            cout << "\"And a blessing for the crossing, pilgrim.\"\n";
        }
        cout << "The boat pushes off. You reach the far shore.\n";
    }
    else if (coins >= 30 && hasToken)
    {
        // Compound condition: a middling Smuggler with the token still crosses.
        cout << "\"Half fare, but that token buys the rest. Quietly, now.\"\n";
    }
    else if (coins >= 30)
    {
        cout << "\"Half fare earns you the shallows crossing. Roll up your boots.\"\n";
    }
    else
    {
        cout << "\"No coin, no boat. The river keeps its bank.\"\n";
    }

    cout << "The ferryman turns back to the water.\n";
    return 0;
}
