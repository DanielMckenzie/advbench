import os
import json
import numpy as np

# List all the experiment folders
folders = [f for f in os.listdir() if os.path.isdir(f)]

# Separate results for original and geometric experiments
results = {"original": {}, "geometric": {}}

# For each experiment folder
for folder in folders:
    print('folder: ', folder)

    # List all the subdirectories in the experiment folder
    subdirs = [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

    # For each subdirectory
    for subdir in subdirs:

        # Construct the path to the results.json file
        file_path = os.path.join(folder, subdir, 'results.json')

        # If the results.json file exists
        if os.path.isfile(file_path):

            # Initialize a list to hold the data from each line in the file
            data = []

            # Open the file and load each line as a separate JSON object
            with open(file_path, 'r') as f:
                for line in f:
                    data.append(json.loads(line))

            # Determine if the experiment is original or geometric
            key = "geometric" if "mod" in subdir else "original"

            # Remove the 'mod' from the experiment name if it exists
            experiment_name = subdir.replace("_mod", "")

            # If the experiment name is not already in the results dictionary, add it
            if experiment_name not in results[key]:
                results[key][experiment_name] = {name: [] for name in data[0]['Test'].keys() if 'Accuracy' in name}

            # Find the epoch with the best validation augmented accuracy
            best_epoch = max(data, key=lambda x: x['Validation']['Clean-Accuracy'])

            # Record all the test accuracies at the best epoch
            for name, value in best_epoch['Test'].items():
                if 'Accuracy' in name:
                    results[key][experiment_name][name].append(value)

# For each experiment in the results
for experiment in results["geometric"].keys():
    # For each accuracy in the results
    for accuracy in results["geometric"][experiment].keys():

        # Calculate the mean and standard deviation of the test accuracies for the geometric experiment
        mean_accuracy_mod = np.mean(results["geometric"][experiment][accuracy])
        # print('results["geometric"][experiment][accuracy]: ', results["geometric"][experiment][accuracy])
        std_accuracy_mod = np.std(results["geometric"][experiment][accuracy])

        # Calculate the mean and standard deviation of the test accuracies for the original experiment
        mean_accuracy_orig = np.mean(results["original"][experiment][accuracy])
        # print('results["original"][experiment][accuracy]: ', results["original"][experiment][accuracy])
        std_accuracy_orig = np.std(results["original"][experiment][accuracy])

        # Print the results
        print(f'{experiment} - {accuracy}: {mean_accuracy_orig:.2f}  (original), {mean_accuracy_mod:.2f}  (geometric)')
