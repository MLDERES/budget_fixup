import pandas as pd

# This function will parse the 'work tags' column into separate columns
#  it's called as a vector operation on the 'work tags' column
def parse_work_tags(work_tags):
    tag_dict = {}
    lines = work_tags.split('\n')
    for line in lines:
        if line.strip():  # Skip empty lines
            tag_name, tag_value = line.strip().split(': ')
            tag_dict[tag_name] = tag_value
    return tag_dict

# Assign the path where the files exists
# Load the Excel file
def parse_work_tags_column(input_file_path, output_file_path):
    df = pd.read_excel(input_file_path)

    # Apply the parse_work_tags function to the 'work tags' column and expand it into separate columns
    df_worktags = df['Worktags'].apply(parse_work_tags).apply(pd.Series)

    # Concatenate the original DataFrame with the parsed work tags columns
    result_df = pd.concat([df, df_worktags], axis=1)

    # Drop the original 'work tags' column if needed
    columns_to_drop = ['Worktags','Accounting Date', 'Operational Transaction', 'Journal',
       'Revenue Category','AASIS Code', 'Cost Center', 'Designated','Earning', 'Employee Type', 'Fund', 'Job Profile',
       'Location', 'NACUBO Function', 'Pay Group', 'Pay Rate Type','Personnel Services Restrictions', 'Position', 'Deduction (Workday Owned)', 'Fringe Basis']
    result_df.drop(columns=columns_to_drop, inplace=True,errors='ignore')

    result.df.to_excel(output_file_path, index=False)