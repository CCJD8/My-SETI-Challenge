import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import zipfile
import ibmseti
import getopt


def take_spectrogram_log(spectrogram, log_option):
    """Take logarithm of spectrogram. Ensure that there are no values less than or equal to zero."""
    if log_option:
        spectrogram_pos_min = spectrogram[spectrogram > 0].min()
        spectrogram[spectrogram <= 0] = spectrogram_pos_min
        return np.log(spectrogram)
    else:
        return spectrogram


def to_json(header):
    """Convert header (type: python dict) to json."""
    uuid = header['uuid']
    signal_classification = header['signal_classification']
    return {'uuid':uuid, 'signal_classification':signal_classification}


def main(argv):
    """Main function that takes the command line arguments and creates the spectrograms."""
    input_dir = '.'
    output_dir = '.'
    log_option = True
    usagestring = "convert_to_spectrographs.py -i <indir> -o <outdir> -l <logOpt>"
    my_data_folder = os.getcwd() + '/'
    if os.path.exists(my_data_folder) is False:
        os.makedirs(my_data_folder)
    
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
    dataset = zipfile.ZipFile("C:/Users/Connor/Documents/Nebuchadnezzar/Learning/Python/Summer-2025/Simulated-Data-Zip.zip")
    all_data_files = dataset.namelist()
    
    print('Input dir is ', input_dir)
    print('Output dir is ', output_dir)
    print('Log option is ', log_option)
    
    # Create figure and axes for spectrogram
    fig, ax = plt.subplots(figsize=(10, 5))
    
    all_headers_dict = {}
        
    # Create spectrograms by reading .dat files with ibmseti and save as png
    for idx, current_file in enumerate(all_data_files):
        if idx >= 20:
            break
        read_file = ibmseti.compamp.SimCompamp(dataset.open(current_file, 'r').read())
        spectrogram = read_file.get_spectrogram()
        header = read_file.header()
        ax.imshow(take_spectrogram_log(spectrogram, log_option), aspect=(0.5*float(spectrogram.shape[1]) / spectrogram.shape[0]), cmap="gray")
        ax.yaxis.set_inverted(False)
        
        ax.set_title(str(current_file).split("/")[1])
        ax.set_xlabel("Time")
        ax.set_ylabel("Frequency")
                
        pngname,_ = os.path.splitext(os.path.basename(current_file))  
        pngname = pngname + '.png'
        fig.savefig(os.path.join(output_dir, pngname), bbox_inches='tight')
        
        ax.cla()
        
        print(header)
        
        all_headers_dict.setdefault(header['signal_classification'], []).append(header)
                

    # Create full set of training and test data. Ensure there is the same amount of each signal type
    training_percentage = 0.75
    test_percentage = 0.25
    full_training_set = {}
    full_test_set = {}
        
    # Loop through dictionary which contains all data headers
    # NB: [ERROR] we get duplicates in the test and train data when the training or testing sizes round to zero
    for signal_type, uuid in all_headers_dict.items():
        total_size = len(signal_type)
        training_size = int(total_size * training_percentage)
        test_size = int(total_size * test_percentage)
        
        training_set = uuid[:training_size]
        test_set = uuid[-1*test_size:]
        
        full_training_set[signal_type] = training_set
        full_test_set[signal_type] = test_set
        
            
    max_zip_file_size_in_mb = 25
    
    # Create folders for png and zip files
    png_file_folder = my_data_folder + "/pngfiles"
    if os.path.exists(png_file_folder) is False:
        os.makedirs(png_file_folder)
    zip_file_folder = my_data_folder + "/zipfiles/"
    if os.path.exists(zip_file_folder) is False:
        os.makedirs(zip_file_folder)
    
    
    # header_list is a list. Each item in the list is a header dictionary of a particular spectrogram
    # TRAINING: Create the .zip files which contain the .png spectrograms.
    for signal_type, header_list in full_training_set.items():
        file_names = []
        count = 1
        
        for i in range(len(header_list)):
            name = png_file_folder + '/' + header_list[i]['uuid'] + ".png"
            file_names.append(name)

        for file in file_names:
            print(zip_file_folder)
            archive_name = f"{zip_file_folder}_{count}_{signal_type}.zip"
            #print(f"You are attempting to save to:\n{archive_name}")
            if os.path.exists(archive_name):
                zz = zipfile.ZipFile(archive_name, mode='a')
            else:
                zz = zipfile.ZipFile(archive_name, mode='w')
                
            zz.write(file)
            zz.close()
            
            if os.path.getsize(archive_name) > max_zip_file_size_in_mb * 1024 ** 2:
                count += 1
                

# Ensure the program is run only when run directly by checking 
# if __name__ == "__main__". If true, the main() function is called 
# and the command line arguments are passed (excluding the script
# name itself) using sys.argv[1:].
if __name__ == "__main__":
    main(sys.argv[1:])
