// we can't structure statments like (1+2)+1
// but we can do the opposite direction

int myval = 2;
int val2 = (1+2-3+4)+3;
int val3 = (65)+(66);

int val;
int my_val = 74+89;
int my_other_val;

int main() {
    val3 = val2 + 2;
    return 0;
}

// OMG we support functions with statements!!!
void test() {
    int val2;
    
    // Assignments can't be expressions yet, working on it tho
    int val3 = 1;
}

int anotherTest() {
    int val4 = 1;

    // Return type checking doesn't work yet
    return 1;
}

