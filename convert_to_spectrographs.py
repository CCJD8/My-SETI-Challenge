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
    """Main function that takes the command line arguments and creates the spectrograms."""
    input_dir = '.'
    output_dir = '.'
    log_option = True
    usagestring = "convert_to_spectrographs.py -i <indir> -o <outdir> -l <logOpt>"
    
    # Use getopt() to parse command line options and parameter list. 
    # The first return is a list of (option, value) pairs, 
    # the second is a list of program arguments left after
    # the option list was stripped.
    try:
        options, _ = getopt.getopt(argv,"hi:o:l:s:m:",["indir=","outdir=","log=","skip=","m="])
    except getopt.GetoptError:
        print(f"Error in command line input format\n{usagestring}")
        sys.exit()
                
    # Loop through the options and their values to assign input/output directories etc
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
    
    # Create figure and axes for spectrogram
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Create spectrograms by reading .dat files with ibmseti and save as png
    for current_file in all_data_files:
        spectrogram = ibmseti.compamp.SimCompamp(dataset.open(current_file, 'r').read()).get_spectrogram()
        ax.imshow(take_spectrogram_log(spectrogram, log_option), aspect=(0.5*float(spectrogram.shape[1]) / spectrogram.shape[0]), cmap="gray")
        ax.yaxis.set_inverted(False)
        
        ax.set_title(str(current_file).split("/")[1])
        ax.set_xlabel("Time")
        ax.set_ylabel("Frequency")
                
        pngname,_ = os.path.splitext(os.path.basename(current_file))  
        pngname = pngname + '.png'
        fig.savefig(os.path.join(output_dir, pngname), bbox_inches='tight')
        
        ax.cla()


# Ensure the program is run only when run directly by checking 
# if __name__ == "__main__". If true, the main() function is called 
# and the command line arguments are passed (excluding the script
# name itself) using sys.argv[1:].
if __name__ == "__main__":
    main(sys.argv[1:])