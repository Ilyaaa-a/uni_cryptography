#include <iostream>
#include <string>

char shiftChar(char c, int k) {
    k = ((k % 26) + 26) % 26;  // нормализация: отрицательный ключ -> положительный 
    if (c >= 'a' && c <= 'z') return static_cast<char>('a' + (c - 'a' + k) % 26);  // a = 97 z = 122
    if (c >= 'A' && c <= 'Z') return static_cast<char>('A' + (c - 'A' + k) % 26); // A = 65 Z = 90
    return c;
}

std::string encrypt(const std::string& s, int k) {
    std::string out;
    out.reserve(s.size());
    for (char c : s) out += shiftChar(c, -k);
    return out;
}

std::string decrypt(const std::string& s, int k) {
    return encrypt(s, k);
}

void bF(const std::string& cipher) {
    for (int k=0; k<26; ++k){
        std::cout << "k=" << k << ": " << decrypt(cipher, k) << '\n';
    }
}

const double FREQ[26] = {
    8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0,     // a-i
    0.16, 0.77, 4.0, 2.4, 6.7, 7.5, 1.9, 0.12, 6.0,   // j-r
    6.3, 9.1, 2.8, 0.98, 2.4, 0.15, 2.0, 0.074        // s-z
};

std::string TRUEhack(const std::string& cipher){
    int counts[26] = {0};
    int total = 0;
    for (char c : cipher) {
        if (c >= 'a' && c <= 'z') { counts[c - 'a']++; total++;}
        else if (c >= 'A' && c <= 'Z') { counts[c - 'A']++; total++; }
    }
    if (total == 0) return cipher;

    int best = 0;
    double bestScore = 1e18;
    for (int k = 0; k < 26; ++k) {
        double score = 0.0;
        for (int i = 0; i < 26; ++i) {
            double observed = counts[(i + k) % 26];
            double expected = FREQ[i] / 100.0 * total;
            score += (observed - expected) * (observed - expected) / expected;
        }
        if (score < bestScore) {
            bestScore = score;
            best = k;
        }
    }

    std::string result;
    for (char c : cipher) {
        if (c >= 'a' && c <= 'z')
            result += static_cast<char>('a' + (c - 'a' - best + 26) % 26);
        else if (c >= 'A' && c <= 'Z')
            result += static_cast<char>('A' + (c - 'A' - best + 26) % 26);
        else
            result += c;   
    }
    return result;
}

int main() {
    std::string text;
    int k;
    std::cout << "Text: ";
    std::getline(std::cin, text);
    std::cout << "Key: "; 
    std::cin >> k;

    std::string enc = encrypt(text, k);
    std::cout << "Encrypted: " << enc << '\n';
    // std::cout << "Decrypted: " << bF(enc, k) << '\n'; 
    std::cout << "Decrypted2: " << TRUEhack(enc) << '\n';
}
