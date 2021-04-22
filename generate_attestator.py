#!/usr/bin/python
import argparse
import os
import string
import sys

# Generate the default attestator
def generate_default(output_dir, label, degradation_label):
  codeguard_dir = os.path.dirname(sys.argv[0])# The directory that contains the python scripts and the source code that will be injected
  attestator_dst = os.path.join(output_dir, 'attestator_' + label + '.c')
  attestator_variables_dst = os.path.join(output_dir, 'attestator_variables_' + label + '.c')

  if not os.path.exists(attestator_dst):
    attestator_src = os.path.join(codeguard_dir, 'attestator.c')
    instantiate_template(attestator_src, attestator_dst, label, degradation_label)
  if not os.path.exists(attestator_variables_dst):
    attestator_variables_src = os.path.join(codeguard_dir, 'attestator_variables.c')
    instantiate_template(attestator_variables_src, attestator_variables_dst, label, degradation_label)

# Instantiate the template by filling in the labels in the input file and writing the new output file
def instantiate_template(input_file, output_file, label, degradation_label):
  # Open the input and output file (the output file will be overwritten if it already exists)
  with open(input_file) as f_in:
    with open(output_file, 'w+') as f_out:
      for line in f_in:
        line = string.replace(line, '##LABEL##', label)
        line = string.replace(line, '##DEGRADATION_LABEL##', degradation_label)

        # Write out the line
        f_out.write(line)

def main():
  # Parsing the arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input_file', required=True, help='The input file. This file contains the labels we need to replace.')
  parser.add_argument('-o', '--output_file', required=True, help='The output file.')
  parser.add_argument('-l', '--label', required=True, help='The label for the attestator.')
  parser.add_argument('-d', '--degradation_label', required=True, help='The label for the start_degradation function.')
  args = parser.parse_args()

  # Generate the actual file
  instantiate_template(args.input_file, args.output_file, args.label, args.degradation_label)

if __name__ == "__main__": main()
