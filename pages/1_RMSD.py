import streamlit as st
import os
import io
import subprocess
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "PDBtoFASTA"))

from rmsd import Pdb

st.markdown("## RMSD")
st.divider()

# File uploaders
pdb_file1 = st.file_uploader(
    "Upload",
    type="pdb", key="1",
    help="**Input:** Protein PDB (Both structures must contain the same number of atoms in similar order.) \n\n**Output:** RMSD Value"
)

pdb_file2 = st.file_uploader(
    "Upload",
    type="pdb", key="2",
    help="**Input:** Protein PDB (Both structures must contain the same number of atoms in similar order.) \n\n**Output:** RMSD Value"
)

# Optional
ligand = st.checkbox("Ligand (HETATM) atoms",
                              value=False,
                              help="If checked, it calculates RMSD between ligand (HETATM) atoms."
                    )

carbon = st.checkbox("Carbon atoms",
                              value=False,
                              help="If checked, it calculates RMSD between carbon atoms only."
                    )

calpha = st.checkbox("Alpha-Carbon atoms",
                              value=False,
                              help="If checked, it calculates RMSD between alpha-carbon atoms only."
                    )

# File Processing
if pdb_file1 is not None and pdb_file2 is not None:
    run_button = st.button("Run", help="Calculating RMSD")
    if run_button:
        with st.spinner("Running..."):
            time.sleep(2)
            # Save files
            pdb_path1 = "./protein1.pdb"
            pdb_path2 = "./protein2.pdb"
            
            # Read file values
            pdb_data1 = pdb_file1.getvalue()
            pdb_data2 = pdb_file2.getvalue()

            with open(pdb_path1, "wb") as f:
                f.write(pdb_data1)
            with open(pdb_path2, "wb") as f:
                f.write(pdb_data2)
            
                
            # Run script via subprocess
            cmd_args = ["python", "rmsd.py", "protein1.pdb", "protein2.pdb"]
            
            if ligand:
                cmd_args.append("-l")

            if carbon:
                cmd_args.append("-c")

            if calpha:
                cmd_args.append("-ca")

            result = subprocess.run(cmd_args, capture_output=True, text=True)

            # Display the output
            st.divider()
            st.subheader("Output")
            st.write("RMSD Value is:")
            st.code(result.stdout)
            
            

