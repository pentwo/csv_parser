import os

from csv_to_json import csv_categorize

# User input for folder name
folder_name = input("Please input a folder name: ")


def load_files_and_categorize(folder_name):
    input_folder = os.path.join(folder_name, "csv")
    output_folder = os.path.join(folder_name, "json")

    os.makedirs(output_folder, exist_ok=True)

    # List all CSV files in the input directory
    csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

    for csv_file in csv_files:
        print(f'Loading CSV: {csv_file}')
        csv_categorize(
            input_folder=input_folder,
            output_folder=output_folder,
            csv_file=csv_file
        )


load_files_and_categorize(folder_name)
