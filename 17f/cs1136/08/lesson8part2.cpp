// Jared Mosley jlm141230
#include <stdio.h>
#include <iostream>
#include <iomanip>

using namespace std;

// convert temperature from farenheit to celsius
double convert(double fahrenheit){
    return (fahrenheit - 32.0) / 1.8;
}

// read in two values
void read(double &lower, double &upper, double &increment) {
    bool valid = false;
    // loop until the user input is valid
    while(!valid){
        cin >> lower;
        cin >> upper;
        cin >> increment;
        // check the values
        if (increment > 0.0 && lower <= upper) {
            valid = true;
        }
        else {
            cout << "Starting temperature must be <= ending temperature and increment must be > 0.0" << endl;
        }
    }
}

// display the temperature increments
void display(double lower, double upper, double increment) {
    cout << "     Fahrenheit        Celsius" << endl;
    // loop from lower to upper along the increment and display both the C and F values
    double j = 0;
    for(int i = 0; i*increment <= upper-lower; i++){
        // start a new line after 15 characters
        j = lower + i*increment;
        cout << setw(15) << setprecision(3) << fixed << (j);
        cout << setw(15) << setprecision(3) << fixed << convert(j) << endl;
    }
}

// main function
int main(){
    double lower;
    double upper;
    double increment;

    read(lower, upper, increment);
    display(lower, upper, increment);

    return 0;
}
