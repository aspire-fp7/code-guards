#!/usr/bin/python
import argparse
import string

# This script takes the following arguments:
# Argument 1: Input file. The file that contains the labels we need to replace.
# Argument 2: Output file where the labels have been replaced.
# Argument 3: The label.

def generate(input_file, output_file, label, degradation_label):
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
  generate(args.input_file, args.output_file, args.label, args.degradation_label)

if __name__ == "__main__": main()
