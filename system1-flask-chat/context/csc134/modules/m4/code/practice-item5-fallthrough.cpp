// practice-item5-fallthrough.cpp — M4 Practice exit ticket, Item 5 (classify-the-error)
//
// GATE: EXPECT-WARNING
//
// BROKEN ON PURPOSE: exactly one flaw — a missing `break` after case 1, so case 1
// falls through into case 2. It compiles and runs; it just does the wrong thing.
//
// This file is NOT held to the zero-warning bar, and the marker above tells the
// compile gate so. On GCC (what Codespaces runs) it emits:
//     warning: this statement may fall through [-Wimplicit-fallthrough=]
// Apple clang stays silent, because it does not enable that warning under
// -Wall -Wextra. Either way the program BUILDS and RUNS and prints the wrong
// thing, which is what makes Item 5's answer "Logic" and not "Syntax" — a
// warning does not stop a build; an error would have left nothing to run.
//
// Do not add the `break;`. Do not add [[fallthrough]]. Breaking this file
// "correctly" destroys the exit-ticket item it exists to support.
//
// Students never compile this — Item 5 is a read-only predict/classify item.
// The file exists so the printed listing is provably the behaviour described.
//
// Build (to see output): g++ -std=c++17 -o practice-item5-fallthrough practice-item5-fallthrough.cpp
// (the course flags are omitted on purpose here; see the marker above)
#include <iostream>
using namespace std;

int main()
{
    int potion = 1;   // author wants ONLY the red-potion line to print

    switch (potion)
    {
        case 1:
            cout << "Red potion: +10 health.\n";
        case 2:
            cout << "Blue potion: +10 mana.\n";
            break;
        default:
            cout << "No potion.\n";
    }

    return 0;
}
