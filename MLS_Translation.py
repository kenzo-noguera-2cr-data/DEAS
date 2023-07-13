import os
import pandas as pd

def transform_csv(input_filename):
    # Extract the directory and listing name from the input filename
    directory = os.path.dirname(input_filename)
    base_name = os.path.basename(input_filename)
    listing_name = os.path.splitext(base_name)[0].replace("_RID", "")

    # Output filename based on the listing name and directory
    output_filename = os.path.join(directory, f"{listing_name}_MLS_Data.csv")

    # Load the input CSV
    input_df = pd.read_csv(input_filename)

    # Load the translation CSV
    translation_df = pd.read_csv("MLS_Translation.csv")

    # Merge the input and translation dataframes based on the ATTRIBUTE column
    merged_df = pd.merge(input_df, translation_df, left_on="ATTRIBUTE", right_on="2CR_INTERNAL_ID")

    # Replace the ATTRIBUTE column values with the corresponding POINT2IDS column values
    merged_df["ATTRIBUTE"] = merged_df["MLS_IDS"]

    # Keep only the ATTRIBUTE, VALUE, and VALUE_TYPE columns
    merged_df = merged_df[["ATTRIBUTE", "VALUE", "VALUE_TYPE"]]

    # Load the additional rows from the CSV file
    additional_rows_df = pd.read_csv("fixed_info_mls.csv")

    # Concatenate the merged DataFrame with the additional rows DataFrame
    merged_df = pd.concat([merged_df, additional_rows_df], ignore_index=True)

    # Load the value_type_dict CSV into a DataFrame
    value_type_dict = pd.read_csv("VALUE_TYPE_DICT.csv")

    # Merge the merged_df with value_type_dict based on ATTRIBUTE column
    merged_df = pd.merge(merged_df, value_type_dict, on='ATTRIBUTE', how='left')

    # Update VALUE_TYPE column with corresponding values from value_type_dict
    merged_df['VALUE_TYPE'] = merged_df['VALUE_TYPE_y']
    merged_df.drop('VALUE_TYPE_y', axis=1, inplace=True)

    merged_df = merged_df[["ATTRIBUTE", "VALUE", "VALUE_TYPE_x"]]

    merged_df.rename(columns={'VALUE_TYPE_x': 'VALUE_TYPE'}, inplace=True)

    # Save the merged dataframe as the output CSV with specific column dtypes as strings
    merged_df.to_csv(output_filename, index=False)

    print("Data has been transformed and saved as", output_filename)

transform_csv(r"C:\Users\Kenzo Noguera\Desktop\APP PROJECT\Code\Selenium_Version\Curridabat Torres de Granadilla\Curridabat Torres de Granadilla_RID.csv")