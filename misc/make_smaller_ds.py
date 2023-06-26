import os
import shutil

# Source folder containing the .flac audio files
source_folder = './audio'

# Destination folder for the selected files
destination_folder = './small_dataset'

# Ensure the destination folder exists, or create it if necessary
os.makedirs(destination_folder, exist_ok=True)

# Iterate over the files in the source folder
for filename in os.listdir(source_folder):
    if filename.endswith('.flac'):
        # Split the filename into its components
        components = filename.split('_')
        print('components:', components)
        
        # Extract the necessary information
        lang = components[0]
        digit = components[3]
                
        # Check if the file satisfies the criteria (lang=english and digit=0, 1, 2, or 3)
        if lang == 'lang-english' and digit in ['digit-0.flac', 'digit-1.flac', 'digit-2.flac', 'digit-3.flac']:
            # Get the source file path
            source_file = os.path.join(source_folder, filename)
            
            # Get the destination file path
            destination_file = os.path.join(destination_folder, filename)
            
            # Copy the file to the destination folder
            shutil.copy2(source_file, destination_file)