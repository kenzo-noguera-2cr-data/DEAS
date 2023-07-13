import os
import pandas as pd

def transform_csv(input_filename):
    # Extract the directory and listing name from the input filename
    directory = os.path.dirname(input_filename)
    base_name = os.path.basename(input_filename)
    listing_name = os.path.splitext(base_name)[0].replace("_RID", "")

    # Output filename based on the listing name and directory
    output_filename = os.path.join(directory, f"{listing_name}_Point2_Data.csv")

    # Load the input CSV
    input_df = pd.read_csv(input_filename)

    # Load the translation CSV
    translation_df = pd.read_csv("Point2_Translation.csv")

    # Merge the input and translation dataframes based on the ATTRIBUTE column
    merged_df = pd.merge(input_df, translation_df, left_on="ATTRIBUTE", right_on="2CR_INTERNAL_ID")

    # Replace the ATTRIBUTE column values with the corresponding POINT2IDS column values
    merged_df["ATTRIBUTE"] = merged_df["POINT2IDS"]

    # Keep only the ATTRIBUTE and VALUE columns
    merged_df = merged_df[["ATTRIBUTE", "VALUE"]]

    # Save the merged dataframe as the output CSV
    merged_df.to_csv(output_filename, index=False)

    print("Data has been transformed and saved as", output_filename)

transform_csv(r"C:\Users\Kenzo Noguera\Desktop\APP PROJECT\Code\Selenium_Version\Curridabat Torres de Granadilla\Curridabat Torres de Granadilla_RID.csv")
