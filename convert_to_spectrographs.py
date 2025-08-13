import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import zipfile
import ibmseti
import getopt


def take_spectrogram_log(spectrogram, log_option):
    """Take logarithm of spectrograph."""
    if log_option:
        return np.log(spectrogram)
    else:
        return spectrogram


def main(argv):
    """Main function that takes the command line arguments."""
    input_dir = '.'
    output_dir = '.'
    log_option = True
    skip_lines = 2
    usagestring = "convert_to_spectrographs.py -i <indir> -o <outdir> -l <logOpt> -s <skip> -m <spectrogram height factor>"
    
    # Create figure and axes for spectrogram
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Use getopt() to parse command line options and parameter list. 
    # The first return is a list of (option, value) pairs, 
    # the second is a list of program arguments left after
    # the option list was stripped.
    try:
        options, arguments = getopt.getopt(argv,"hi:o:l:s:m:",["indir=","outdir=","log=","skip=","m="])
    except getopt.GetoptError:
        print(f"Error in command line input format\n{usagestring}")
        sys.exit()
                
    for opt, arg in options:
        if opt in ("-o", "--outdir"):
            output_dir = arg
        elif opt in ("-i", "--indir"):
            input_dir = arg
        elif opt in ("-l", "--log"):
            if arg == "True":
                log_option = True
            else:
                log_option = False
        elif opt in ("-s", "--skip"):
            skipLines = int(arg)
        elif opt in ("-m", "--m"):
            m = int(arg)
        else:
            print("Error in command line input format")
            print(usagestring)
            sys.exit()
    
    
    # Read the .zip file with zipfile
    dataset = zipfile.ZipFile("C:/Users/Connor/Documents/Nebuchadnezzar/Learning/Python/Summer-2025/Simulated Data Zip.zip")
    all_data_files = dataset.namelist()
    
    print('Input dir is ', input_dir)
    print('Output dir is ', output_dir)
    print('Log option is ', log_option)
    
    # Create spectrograms and save as png
    for current_file in all_data_files:
        spectrogram = ibmseti.compamp.SimCompamp(dataset.open(current_file, 'r').read()).get_spectrogram()
        ax.cla()
        ax.imshow(take_spectrogram_log(spectrogram, log_option), aspect=(0.5*float(spectrogram.shape[1]) / spectrogram.shape[0]))
        
        pngname,_ = os.path.splitext(os.path.basename(current_file))  
        pngname = pngname + '.png'
        fig.savefig(os.path.join(output_dir, pngname), bbox_inches='tight')


if __name__ == "__main__":
    main(sys.argv[1:])