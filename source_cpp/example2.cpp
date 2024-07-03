Ciphertext fun(Ciphertext a) {
    // Create FHE circuit
    auto b = -a + 2;
    auto c = a;

    for (int i = 0; i < 5; ++i) {
        c = c * (-c + 2);
        b = b * (-c + 2);
    }

    auto d = b.mean() + c.mean();
    return d;
}

int main() {
    FheProgram program("CKKS", {1});

    Ciphertext a = program.add_secret("a", 40);

    auto d = fun(a);
    program.cppcompile(d);

    return 0;
}