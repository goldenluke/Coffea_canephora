from multi_dataset import generate_all
from compare_engine import compare
from gpu_bifurcation import generate

print("1. Gerando datasets...")
generate_all()

print("2. Comparando cenários...")
compare()

print("3. Gerando bifurcação GPU...")
generate()

print("DONE")
