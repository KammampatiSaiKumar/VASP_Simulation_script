import os
import subprocess
import shutil

i_values = [0, 0.4, 0.8, 1.2, 1.6, -0.4, -0.8, -1.2, -1.6]
current_dir = os.getcwd()
files_to_copy = ['INCAR_relax','POSCAR' ,'INCAR_dos', 'POTCAR', 'KPOINTS']
for i in i_values:
    dirname = f"Cu_{i:.1f}"
    os.makedirs(dirname, exist_ok=True)
    for file_name in files_to_copy:
        source_path = os.path.join(current_dir, file_name)
        destination_path = os.path.join(current_dir, dirname, file_name)
        shutil.copy(source_path, destination_path) 
    print(f"Directory '{dirname}' created and files copied.")
directories1 = {
    "Cu_0.0": 0.000,
    "Cu_0.4": 0.004,
    "Cu_0.8": 0.008,
    "Cu_1.2": 0.012,
    "Cu_1.6": 0.016,
    "Cu_-0.4": -0.004,
    "Cu_-0.8": -0.008,
    "Cu_-1.2": -0.012,
    "Cu_-1.6": -0.016,
}
for dir_name, multiplier in directories1.items():
    poscar_path = os.path.join(dir_name, "POSCAR")  
    
    if os.path.exists(poscar_path):
        # Read the contents of the POSCAR file
        with open(poscar_path, 'r') as file:
            lines = file.readlines()

        # Extract and modify the value on the second line
        actual_value = float(lines[1].strip())
        new_value = actual_value + multiplier * actual_value
        lines[1] = f"{new_value:.6f}\n"

        # Write the modified contents back to the POSCAR file
        with open(poscar_path, 'w') as file:
            file.writelines(lines)
        
        print(f"Updated {poscar_path} with new value {new_value:.6f}")
    else:
        print(f"POSCAR file not found in {dir_name}")


directories = ["Cu_0.0", "Cu_0.4", "Cu_0.8", "Cu_1.2", "Cu_1.6", "Cu_-0.4", "Cu_-0.8", "Cu_-1.2", "Cu_-1.6"]

for dirname in directories:
    dir_path = os.path.join(current_dir, dirname)

    # Check if the directory exists before attempting to process it
    if os.path.isdir(dir_path):
        os.chdir(dir_path)  # Change to the directory
        # Run the command
        if os.path.exists('POSCAR') and os.path.exists('INCAR_relax') and os.path.exists('INCAR_dos') and os.path.exists('POTCAR') and os.path.exists('KPOINTS'):
            os.system('mv INCAR_relax INCAR')
            os.system('mpirun -np 48 vasp_std')
            print('relaxed over')
            os.system('mv INCAR_dos INCAR')
            os.system('mpirun -np 48 vasp_std')    
        os.chdir(current_dir)  # Change back to the original directory
    else:
        print(f"Directory '{dirname}' does not exist. Skipping...")

