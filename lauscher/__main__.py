"""
LAUSCHER – Flexible Auditory Spike Conversion Chain

Reference: https://arxiv.org/abs/1910.07407
"""

import argparse
import logging
import os
from os.path import isfile
import matplotlib.pyplot as plt

from lauscher.audiowaves import FileMonoAudioWave
from lauscher.helpers import CommandLineArguments
from lauscher.transformations.wave2spike import Wave2Spike


def main(args,
        input_file: str,
        output_file: str,
        num_channels: int):
    if not isfile(input_file):
        raise IOError(f"Input file '{input_file}' not found.")

    trafo = Wave2Spike(num_channels=num_channels, args=args)
    spikes = FileMonoAudioWave(input_file).transform(trafo)
    _, ax = plt.subplots()
    spikes.plot(ax)
    spikes.export(output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", type=str,
                        help="Path to the input wave file, to be converted to"
                             "a spike train.")
    parser.add_argument("output_file", type=str,
                        help="Path to the output file, spike trains will ber"
                             "written into it.")
    parser.add_argument("--num_channels", type=int, default=700,
                        help="Number of frequency selective channels.")
    parser.add_argument("-j", "--jobs", type=int, default=None,
                        help="Number of concurrent jobs used for data "
                             "processing.")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    
    # Model parameters
    # BM model 
    parser.add_argument("--bm_channels", type=int, default=700,
                        help="Number of frequency selective channels in the BM.")   #???
    parser.add_argument("--bm_a", type=int, default=3500,
                        help="Greenwoods constant.")
    parser.add_argument("--bm_alpha", type=float, default=3.0,
                        help="Attenuation factor.")
    parser.add_argument("--bm_rho", type=float, default=1.0,
                        help="Parameter in deriv of velocity.")
    parser.add_argument("--bm_c", type=float, default=3.5,
                        help="EXPL.")
    parser.add_argument("--bm_c0", type=float, default=10e8,
                        help="Stiffness constant.")
    parser.add_argument("-bm_de", type=float, default=0.15,
                        help="EXPL.")
    parser.add_argument("--bm_h", type=float, default=0.1,
                        help="Height of scaling.")
    parser.add_argument("--bm_m", type=float, default=0.05,
                        help="Effective mass.")
    
    # HC model
    parser.add_argument("--hc_y", type=float, default=5.05,
                        help="Replenishing rate.")
    parser.add_argument("--hc_g", type=float, default=2000.0,
                        help="Max. permeability.")
    parser.add_argument("--hc_l", type=float, default=2500.0,
                        help="Loss rate.")
    parser.add_argument("--hc_r", type=float, default=6580.0,
                        help="Reuptake rate.")
    parser.add_argument("--hc_x", type=float, default=66.3,
                        help="EXPL.")
    parser.add_argument("--hc_a", type=float, default=5.0,
                        help="Permeability offset.")
    parser.add_argument("--hc_b", type=float, default=300.0,
                        help="Permeability rate.")
    parser.add_argument("--hc_h", type=float, default=50000.0,
                        help="Probability scaling.")
    parser.add_argument("--hc_m", type=float, default=1.0,
                        help="EXPL.")
    
    # BC model
    parser.add_argument("--bc_n_convergence", type=int, default=40,
                        help="Number of hair cells per BM measuring point?.")
    parser.add_argument("--bc_tau_mem", type=float, default=1e-3,
                        help="Membrane time constant.")
    parser.add_argument("--bc_tau_syn", type=float, default=5e-4,
                        help="Synapse time constant.")
    parser.add_argument("--bc_tau_refrac", type=float, default=1e-3,
                        help="Refractory period time constant.")
    parser.add_argument("--bc_weight", type=float, default=13e3,
                        help="weights to the bc.")
    
    
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
        

small_dataset_folder = './small_dataset'

# Iterate over the files in the 'small_dataset' folder
for filename in os.listdir(small_dataset_folder):
    if filename.endswith('.flac'):
        # Get the input file path
        input_file = os.path.join(small_dataset_folder, filename)
        
        # Set the output file name to be the same as the input file name
        output_file = os.path.splitext(filename)[0]
        print('input_file: ', input_file, 'output_file: ', output_file)
        
        # Call the main function for each file
        main(args, input_file, output_file, args.num_channels)

    # global_args = CommandLineArguments()
    # global_args.num_concurrent_jobs = args.jobs
# main(args, args.input_file, args.output_file, args.num_channels)
