// Jared Mosley jlm141230
#include <stdio.h>
#include <iostream>

using namespace std;

// read in two values
void read(unsigned int &lower, unsigned int &upper) {
    bool valid = false;
    // loop until the user input is valid
    while(!valid){
        cout << "Enter lower and upper values" << endl;
        cin >> lower;
        cin >> upper;
        // check the values
        if (lower >= 32 && upper <= 126 && lower <= upper) {
            valid = true;
        }
        else {
            cout << "Values must be in range 32 to 126 inclusive" << endl;
        }
    }
}

// display all ascii characters between lower and upper
void display(unsigned int lower, unsigned int upper) {
    cout << "Characters for ASCII values between " << lower << " and " << upper << endl;
    cout << "----+----+----+-" << endl;
    int flag = 0;
    // loop from lower to upper and display the corresponding ascii characters
    for(unsigned int i = lower; i <= upper; i++){
        // start a new line after 15 characters
        if(flag%16 == 0 && flag != 0){
            flag = 0;
            cout << "\n";
        }
        flag++;
        cout << (char)i;
    }
    cout << "\n----+----+----+-" << endl;
}

// main function
int main(){
    unsigned int lower;
    unsigned int upper;

    read(lower, upper);
    display(lower, upper);

    return 0;
}

