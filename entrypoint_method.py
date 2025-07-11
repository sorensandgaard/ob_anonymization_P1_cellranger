import argparse
import os
import requests
import subprocess

def create_file(out_filename,in_url):
    r = requests.get(in_url, allow_redirects=True)
    open(out_filename, 'wb').write(r.content)

def run_method(output_dir, name, input_files, parameters):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    log_file = os.path.join(output_dir, f'{name}.log.txt')

    # Run Cellranger ctrl
    ref_dir = f"01_references/{parameters[0]}"
    cr_outdir = f"{output_dir}/cellranger_out"
    os.makedirs(cr_outdir, exist_ok=True)

    # Run cellranger through a wrapper that loads the module
    wrapper_path = f"envs/CellRanger-{parameters[1]}_wrapper.sh"

    cr_command = f"{wrapper_path} count --id {name}_first_align --fastqs {input_files}"
    cr_command += f" --output-dir {cr_outdir} --transcriptome {ref_dir}"
    cr_command += f" --create-bam true --expect-cells 15000 --localcores 24 --localmem 100"

    content = f"This is the cellranger command\n{cr_command}\n\n"

    import shutil
    a = shutil.which("cellranger")

    content += f"This is the shutil output\n{a}\n"

    with open(log_file, 'w') as file:
        file.write(content)

    a = subprocess.run(cr_command.split(),capture_output=True,text=True)
    content += f"Cellranger output: (temporarily left out)\n"
    content += a.stdout
    content += f"\n\n"

    # Move BAM file to header folder
    mv_bam_command = f"mv {cr_outdir}/outs/possorted_genome_bam.bam {output_dir}/{name}.possorted.bam"
    a = subprocess.run(mv_bam_command.split(),capture_output=True,text=True)
    content += a.stdout
    
    # Move expression matrix to reference-folder for comparison (faster runtime later) 
    # * Needs edits
    # cp_matrix_command = f"cp -r {cr_outdir}/outs/filtered_feature_bc_matrix {output_dir}/."
    # a = subprocess.run(cp_matrix_command.split(),capture_output=True,text=True)

    # Remove cellranger folder (the data is not needed downstream, and takes up quite a lot of space)
    cleanup_command = f"rm -rf {cr_outdir}"
    a = subprocess.run(cleanup_command.split(),capture_output=True,text=True)
    content += a.stdout

    genome_path = os.path.join(output_dir, f'{name}.refgenome.txt')
    a = subprocess.run(f"touch {genome_path}".split(),capture_output=True,text=True)
    content += a.stdout

    fasta_path = f"{ref_dir}/fasta/genome.fa"
    with open(genome_path, 'w') as file:
        file.write(fasta_path)

    content += f"All clear - successfull run\n"
    with open(log_file, 'w') as file:
        file.write(content)


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Run method on files.')

    # Add arguments
    parser.add_argument('--output_dir', type=str, help='output directory where method will store results.')
    parser.add_argument('--name', type=str, help='name of the dataset')
    parser.add_argument('--R1.counts',type=str, help='input file #1')
    parser.add_argument('--R2.counts',type=str, help='input file #1')

    # Parse arguments
    args, extra_arguments = parser.parse_known_args()

    R1_input = getattr(args, 'R1.counts')
    R2_input = getattr(args, 'R2.counts')
    fastq_paths = os.path.dirname(R1_input) + f"/"

#    process_filtered_input = getattr(args, 'process.filtered')
#    data_counts_input = getattr(args, 'data.counts')
#    data_meta_input = getattr(args, 'data.meta')
#    data_params_input = getattr(args, 'data.data_specific_params')

#    assert process_filtered_input is not None or data_counts_input is not None, "At least one of the values must not be None"
#    data_counts_input = process_filtered_input if process_filtered_input else data_counts_input

    input_files = [R1_input, R2_input]

    # run_method(args.output_dir, args.name, input_files, extra_arguments)
    run_method(args.output_dir, args.name, fastq_paths, extra_arguments)


if __name__ == "__main__":
    main()
