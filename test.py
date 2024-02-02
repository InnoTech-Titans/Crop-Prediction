def read_data():
    excel_file_path = 'data.xlsx'

    # Read the Excel file into a DataFrame
    df = pd.read_excel(excel_file_path)

    ch_values = df[['CH1', 'CH2', 'CH3', 'CH4', 'CH5']]

    # Display the values in columns 'CH1' to 'CH5'
    ch_values_array = ch_values.values
    final_data = ch_values_array[0]
