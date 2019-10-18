#!/usr/bin/python
import argparse
import generate_attestator
import glob
import os
import random
import re
import shutil
import sys

# This script takes the following arguments:
# Argument 1: Input file. The file that contains the annotations we need to process.
# Argument 2: Output file. The processed file.
# Argument 3: The AID.


def process(input_file, output_file, aid):
  # Some initialization for commonly used variables
  codeguard_dir = os.path.dirname(sys.argv[0])# The directory that contains the python scripts and the source code that will be injected
  mechanisms_dir = os.path.join(codeguard_dir, 'mechanisms')
  output_dir = os.path.dirname(output_file)

  # Seed the PRNG using the AID
  random.seed(aid)

  # Compile these regexes that we will use a lot
  reg_attest = re.compile(r'.*#pragma\s*ASPIRE.*guard_attestator.*label\s*\(\s*(?P<id>.*?)\s*\).*')
  reg_verif = re.compile(r'.*#pragma\s*ASPIRE.*guard_verifier.*attestator\s*\(\s*(?P<id>.*?)\s*\).*')
  reg_mechanisms = re.compile(r'mechanisms_(?P<id>.*?).c')

  # Determine the reaction mechanism files available
  degradation_labels = []
  files = os.listdir(mechanisms_dir)
  for f in files:
    match = reg_mechanisms.match(f)
    if (match != None):# If we match the regex, add the label
      if match.group('id') != 'complex':# Temporarily disable the complex mechanisms
        degradation_labels.append(match.group('id'))

  # Open the input and output file (the output file will be overwritten if it already exists)
  contains_annot = False
  with open(input_file) as f_in:
    with open(output_file, 'w+') as f_out:
      for line in f_in:
        # Write out the original line
        f_out.write(line)

        # Randomly choose a degradation to use
        degradation_label = random.choice(degradation_labels)

        # Match for the attestator annotation
        match = reg_attest.match(line)
        if (match != None):# Add a call to an attestator if needed
          label = match.group('id')
          contains_annot = True
          f_out.write('extern void attestator_' + label + '(unsigned int id);\n')
          f_out.write('attestator_' + label + '(0);\n')

          # Generate the attestator for this label (if it doesn't exist already)
          generate_attestator.generate_default(output_dir, label, degradation_label)

        # Match for the verifier annotation
        match = reg_verif.match(line)
        if (match != None):# Add a call to a verifier if needed
          contains_annot = True
          label = match.group('id')
          f_out.write('extern void verifier_' + label + '();\n')
          f_out.write('verifier_' + label + '();\n')

          # Generate the attestator for this label (if it doesn't exist already)
          generate_attestator.generate_default(output_dir, label, degradation_label)

  # If the file contained any annotations, copy the utils over to the output directory (unless this has already happened)
  if contains_annot and not os.path.exists(os.path.join(output_dir, 'utils.c')):
    shutil.copy(os.path.join(codeguard_dir, 'utils.c'), output_dir)
    shutil.copy(os.path.join(codeguard_dir, 'utils.h'), output_dir)

    # Copy all mechanisms stuff
    shutil.copy(os.path.join(mechanisms_dir, 'mechanisms.h'), output_dir)
    for filename in glob.glob(os.path.join(mechanisms_dir, 'mechanisms_*.c')):
      shutil.copy(os.path.join(mechanisms_dir, filename), output_dir)

# Make sure the AID (which is passed as a string containing hexadecimal characters) is automatically converted into an integer
def hex_int(x):
  return int(x, 16)

def main():
  # Parsing the arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('-i', '--input_file', required=True, help='The input file. This file contains the annotations we need to process.')
  parser.add_argument('-o', '--output_file', required=True, help='The output file.')
  parser.add_argument('-a', '--aid', type=hex_int, required=False, help='The AID.')
  args = parser.parse_args()

  # Process the file
  process(args.input_file, args.output_file, args.aid)

if __name__ == "__main__": main()
