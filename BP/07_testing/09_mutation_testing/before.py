# Tema: sin el caso del límite, un mutante puede sobrevivir.
def original(total: int) -> int:
    return total - 10 if total >= 100 else total

def mutant(total: int) -> int:
    return total - 10 if total > 100 else total

def kills_mutant(cases: list[tuple[int, int]]) -> bool:
    return any(mutant(value) != expected for value, expected in cases)

if __name__ == "__main__":
    print(f"Mutant killed: {kills_mutant([(80, 80), (120, 110)])}")
