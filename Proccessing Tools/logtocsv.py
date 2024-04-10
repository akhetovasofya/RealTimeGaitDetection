import os
import csv
# Set the directory path to search for .log files
import global_variables
directory = global_variables.directory

# Iterate through all files in the directory
for filename in os.listdir(directory):
    # Check if the file is a .log file
    if filename.endswith(".log"):
        # Open the .log file for reading
        with open(os.path.join(directory, filename), 'r') as log_file:
            # Read the contents of the file
            log_data = log_file.read()

        # Split the data into rows based on newlines
        rows = log_data.split('\n')

        # Split each row into columns based on commas
        data = [row.split(' ') for row in rows]

        # Skip the first row of data
        data = data[2:-1]

        # Calculate the difference between the value in the first row and each subsequent row
        first_value = float(data[0][0])
        for row in data:
            #print(row)
            value = float(row[0])
            difference = value - first_value
            row.append(str(difference))
        
        # Create a new .csv filename based on the original .log filename
        csv_filename = os.path.splitext(filename)[0] + '.csv'

        # Open a new .csv file for writing
        with open(os.path.join(directory, csv_filename), 'w', newline='') as csv_file:
            # Create a CSV writer object
            writer = csv.writer(csv_file, delimiter=',')

            # Write each row to the CSV file
            for row in data:
                writer.writerow(row)
        # Set the file permissions to allow read and write access for all users
        os.chmod(os.path.join(directory, csv_filename), 0o666)