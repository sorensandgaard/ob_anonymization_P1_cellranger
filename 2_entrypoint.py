import argparse
import os
import requests
import subprocess

# def create_file(out_filename,in_url):
#     r = requests.get(in_url, allow_redirects=True)
#     open(out_filename, 'wb').write(r.content)

def run_method(output_dir, name, fastq_path, parameters):
    # Create the output directory if it doesn't exist
#    os.makedirs(output_dir, exist_ok=True)
    log_file = os.path.join(output_dir, f'{name}.log.txt')

    content = f"All clear - successfull run\n"
    with open(log_file, 'w') as file:
        file.write(content)

    return(1)

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Run method on files.')

    # Add arguments
    parser.add_argument('--output_dir', type=str, help='output directory where method will store results.')
    parser.add_argument('--name', type=str, help='name of the dataset')

    # Parse arguments
    args, extra_arguments = parser.parse_known_args()
    init_reads_paths = "data/"
#     R1_input = getattr(args, 'R1.counts')
#     R2_input = getattr(args, 'R2.counts')
#     fastq_paths = os.path.dirname(R1_input) + f"/"

    run_method(args.output_dir, args.name, init_reads_paths, extra_arguments)

if __name__ == "__main__":
    main()
