//#include <stdio.h>

int main() {
    
    // The following does not compile on gcc 11.2
    // with C17 and below (?)
    // int my_int = 1'000'000;

    printf("Hello, World!");
    
    return 0;
}