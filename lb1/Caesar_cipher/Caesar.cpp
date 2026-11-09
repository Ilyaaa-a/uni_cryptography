#include <iostream>
#include <string>

char shiftChar(char c, int k) {
    k = ((k % 26) + 26) % 26;  // нормализация: отрицательный ключ -> положительный
    if (c >= 'a' && c <= 'z') return static_cast<char>('a' + (c - 'a' + k) % 26);
    if (c >= 'A' && c <= 'Z') return static_cast<char>('A' + (c - 'A' + k) % 26);
    return c;
}

std::string encrypt(const std::string& s, int k) {
    std::string out;
    out.reserve(s.size());
    for (char c : s) out += shiftChar(c, k);
    return out;
}

std::string decrypt(const std::string& s, int k) {
    return encrypt(s, -k);
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
    std::cout << "Decrypted: " << decrypt(enc, k) << '\n';
}
