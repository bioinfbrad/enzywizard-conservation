from __future__ import annotations
from argparse import Namespace, ArgumentParser
from ..services.conservation_service import run_conservation_service

def add_conservation_parser(parser: ArgumentParser) -> None:
    parser.add_argument("-i", "--input_fasta",required=True,help="Path to input cleaned protein sequence file in FASTA format.")
    parser.add_argument("-m", "--input_msa",required=True,help="Path to input multiple sequence alignment (MSA) file prepared by the user.")
    parser.add_argument("-o", "--output_dir",required=True,help="Directory to save output files, including cleaned MSA, HMM profile, and JSON report.")


    parser.set_defaults(func=run_conservation)

def run_conservation(args: Namespace) -> None:
    run_conservation_service(input_fasta=args.input_fasta, input_msa=args.input_msa, output_dir=args.output_dir)
