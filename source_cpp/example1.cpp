Ciphertext fun(Ciphertext a) {
    // Create FHE circuit
    auto b = -a + 2;
    auto c = a - b;

    return b;
}

int main() {
    FheProgram program("CKKS", {1});

    Ciphertext a = program.add_secret("a", 40);

    auto b = fun(a);
    program.cppcompile(b);

    return 0;
}