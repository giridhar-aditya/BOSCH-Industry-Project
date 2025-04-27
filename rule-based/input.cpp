#include <iostream>
using namespace std;

class FortuneMachine {
public:
    void fortune1() {
        cout << "Fortune #1: A new opportunity is coming your way!" << endl;
    }
    void fortune2() {
        cout << "Fortune #2: Someone will bring you good news today." << endl;
    }
    void fortune3() {
        cout << "Fortune #3: You will find what you've been looking for." << endl;
    }
    void fortune4() {
        cout << "Fortune #4: Trust your instincts—they won't fail you." << endl;
    }
    void fortune5() {
        cout << "Fortune #5: A small act of kindness will come back to you." << endl;
    }
    void fortune6() {
        cout << "Fortune #6: You will laugh a lot today—enjoy it!" << endl;
    }
    void fortune7() {
        cout << "Fortune #7: Challenges will make you stronger." << endl;
    }
    void fortune8() {
        cout << "Fortune #8: You are closer to success than you think." << endl;
    }
    void fortune9() {
        cout << "Fortune #9: Good things take time—be patient." << endl;
    }
    void fortune10() {
        cout << "Fortune #10: Your energy is magnetic today!" << endl;
    }
    void unknownFortune() {
        cout << "Invalid number! Pick between 1 and 10." << endl;
    }
};

void showMoodMenu() {
    cout << "\nHow are you feeling today?\n";
    cout << "1. Happy\n";
    cout << "2. Sad\n";
    cout << "3. Excited\n";
    cout << "4. Tired\n";
    cout << "5. Curious\n";
    cout << "Choose your mood (1-5): ";
}

void reactToMood(int mood) {
    if (mood == 1) {
        cout << "Nice! Let's make your day even better!\n";
    } else if (mood == 2) {
        cout << "Cheer up! Here's something for you.\n";
    } else if (mood == 3) {
        cout << "Awesome energy! Let's keep it going.\n";
    } else if (mood == 4) {
        cout << "You deserve a break. Have a peaceful fortune.\n";
    } else if (mood == 5) {
        cout << "Curiosity brings rewards. Let's see your fortune.\n";
    } else {
        cout << "That's not a valid mood. But let's continue!\n";
    }
}

int main() {
    FortuneMachine fm;
    int mood, number, again = 1;
    cout << "====== Fortune Cookie Machine ======\n";
    while (again == 1) {
        showMoodMenu();
        cin >> mood;
        reactToMood(mood);
        cout << "\nPick a number between 1 and 10: ";
        cin >> number;
        if (number == 1) {
            fm.fortune1();
        } else if (number == 2) {
            fm.fortune2();
        } else if (number == 3) {
            fm.fortune3();
        } else if (number == 4) {
            fm.fortune4();
        } else if (number == 5) {
            fm.fortune5();
        } else if (number == 6) {
            fm.fortune6();
        } else if (number == 7) {
            fm.fortune7();
        } else if (number == 8) {
            fm.fortune8();
        } else if (number == 9) {
            fm.fortune9();
        } else if (number == 10) {
            fm.fortune10();
        } else {
            fm.unknownFortune();
        }
        cout << "\nWould you like another fortune? (1 = Yes, 0 = No): ";
        cin >> again;
        cout << "You chose :" << again;
    }
    cout << "\nThanks for using the Fortune Cookie Machine. Goodbye!\n";
    return 0;
}
