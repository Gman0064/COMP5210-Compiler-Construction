// we can't structure statments like (1+2)+1
// but we can do the opposite direction

int myval = 2;
int val2 = (1+2-3+4)+3;
int val3 = (65)+(66);

int val;
int my_val = 74+89;
int my_other_val;

int anotherTest(int input1, int input2) {
    printf(input1+input2);
    val3 = (input1/input2)+74;
    // Return type checking doesn't work yet
    return val3;
}

int val5 = 0;

void main2(){}

// Support for functions with statements inside them
void test() {
    printf(val2+val3);
    for (val5 = 0; val5 < 6; val5++){
        newVal = newVal + val5;
        anotherTest(val1, val2);
    }
    val = 1;
}

int main() {
    int val4 = 0;
    int val5 = 0;
    int val6 = 0;
    // int val4, val6 = 0 does not work
    val3 = val2 + val4;
    anotherTest(val4, val6);
    return val3;
}