# Tema: un caso de frontera detecta el cambio de comportamiento.
def original(total: int) -> int:
    return total - 10 if total >= 100 else total


def mutant(total: int) -> int:
    return total - 10 if total > 100 else total


def kills_mutant(cases: list[tuple[int, int]]) -> bool:
    return any(mutant(value) != expected for value, expected in cases)


if __name__ == "__main__":
    cases = [(80, 80), (100, 90), (120, 110)]
    print(f"Original correct: {all(original(value) == expected for value, expected in cases)}")
    print(f"Mutant killed: {kills_mutant(cases)}")
