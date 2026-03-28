from dataset_generator import generate_dataset
from bifurcation_map import generate_map
from phase_diagram import generate_phase
from paper_generator import generate_paper

print("STEP 1: Gerando dataset...")
generate_dataset()

print("STEP 2: Gerando mapa de bifurcação...")
generate_map()

print("STEP 3: Gerando diagrama de fase...")
generate_phase()

print("STEP 4: Gerando paper...")
generate_paper()

print("DONE — pipeline completo")
