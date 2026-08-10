#include <bits/stdc++.h>
using namespace std;

int main() {
    long long n;
    cin >> n;

    vector<long long> a(n - 1);

    for (long long i = 0; i < n - 1; i++)
        cin >> a[i];

    sort(a.begin(), a.end());

    for (long long i = 0; i < n - 1; i++) {
        if (a[i] != i + 1) {
            cout << i + 1;
            return 0;
        }
    }

        cout << n;

    return 0;
}