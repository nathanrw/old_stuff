#include <iostream>

using namespace std;

struct memberRecord
{
    char memberID[25];
    char fname[25];
    char sname[25];

    int next;
};

struct craftRecord
{
    char BWRegNo[25];
    char memberID[25];
    char name[25];

    int next;
};

struct paymentRecord
{
    char startDate[25];
    char endDate[25];
    char BWRegNo[25];
    bool paid;

    int next;
};

int main()
{

}
