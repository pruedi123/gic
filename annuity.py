# Import necessary libraries
import streamlit as st
import pandas as pd
import math  # Import math module for floor and ceil functions

# Streamlit slider for number of years
number_of_years = st.slider("Select the number of years:", 1, 35, 30, step=1)

# Use number_of_years for the maximum_number_of_years_in_plan
maximum_number_of_years_in_plan = number_of_years

# Add a slider for the income amount
income_amount = st.slider(
    "Select the income amount:", 1000, 100000, 10000, step=1000
)

# Add a slider for the number of recent years to consider
number_of_last_values = st.slider(
    "Select the number of recent years to consider:", 1, number_of_years, 5, step=1
)

# Calculate the maximum number of rows to use based on your original formula
maximum_number_of_rows_of_data_to_use = (
    1166 - (maximum_number_of_years_in_plan * 12)
) + 24

# Load the cpi_end_val.xlsx worksheet
cpi_end_val_df = pd.read_excel("cpi_end_val.xlsx", header=None)

# Limit the DataFrame to the calculated number of rows and the number of years
cpi_isolated_data_df = cpi_end_val_df.iloc[
    :maximum_number_of_rows_of_data_to_use, :maximum_number_of_years_in_plan
]

# Adjust the data based on the selected income amount
adjusted_data_df = cpi_isolated_data_df * income_amount

# Calculate the average of each row (full data corresponding to number_of_years)
row_means_full = (
    adjusted_data_df.mean(axis=1)
    .reset_index(drop=True)
    .to_frame(name="Average Amount Over Time ($)")
)

# Compute statistics for the full data
min_value_full = row_means_full["Average Amount Over Time ($)"].min()
max_value_full = row_means_full["Average Amount Over Time ($)"].max()
median_value_full = row_means_full["Average Amount Over Time ($)"].median()

# Round min, max, and median values for full data
rounded_min_value_full = int(math.floor(min_value_full / 100.0) * 100)
rounded_max_value_full = int(math.ceil(max_value_full / 100.0) * 100)
rounded_median_value_full = int(round(median_value_full / 100.0) * 100)

# Display simplified statistics
st.write("## Overview of Average Amounts Over Total Period")

st.write(f"The Median real spendable income amount historically would have been **${rounded_median_value_full:,.0f}**.")

# Interactive slider for full data with rounded values
selected_value = st.slider(
    "Select a real spendable income to see how likely it would have been to achieve historically",
    rounded_min_value_full,
    rounded_max_value_full,
    value=rounded_median_value_full,
    step=100
)

# Calculate the percentage of scenarios below the selected value (full data)
percentage_below = (row_means_full["Average Amount Over Time ($)"] <= selected_value).mean() * 100
percentage_below = round(percentage_below)  # Round to nearest whole number

st.write(f"Approximately **{percentage_below:.0f}%** of scenarios have an average amount of **${selected_value:,.0f}** or less.")

# Contextual explanation for full data
st.write("### What This Means for You")

st.markdown(f"""
With a fixed income of **${income_amount:,.0f}** over **{number_of_years} years**:

- There's about a **{percentage_below:.0f}%** chance you'll have a real average spending amount of **${selected_value:,.0f}** or less.
""")

# --- For the Last N Values ---

# Extract the last 'number_of_last_values' values from each row
number_of_columns = adjusted_data_df.shape[1]
number_of_last_columns = min(number_of_last_values, number_of_columns)
last_values_df = adjusted_data_df.iloc[:, -number_of_last_columns:]

# Calculate the mean of each row in the last values DataFrame
row_means_last = (
    last_values_df.mean(axis=1)
    .reset_index(drop=True)
    .to_frame(name=f"Recent Average Amount Over Last {number_of_last_columns} Years ($)")
)

# Compute statistics for the last values
min_value_last = row_means_last.iloc[:, 0].min()
max_value_last = row_means_last.iloc[:, 0].max()
median_value_last = row_means_last.iloc[:, 0].median()

# Round min, max, and median values for last values
rounded_min_value_last = int(math.floor(min_value_last / 100.0) * 100)
rounded_max_value_last = int(math.ceil(max_value_last / 100.0) * 100)
rounded_median_value_last = int(round(median_value_last / 100.0) * 100)

# Display simplified statistics for the last values
st.write(f"## Overview of Average Income Amounts (Last {number_of_last_columns} Years)")

st.write(f"The Median spendable (real) income amount was **${rounded_median_value_last:,.0f}**.")

# Interactive slider for last values with rounded values
selected_value_last = st.slider(
    "Select an income result",
    rounded_min_value_last,
    rounded_max_value_last,
    value=rounded_median_value_last,
    step=100
)

# Calculate the percentage of scenarios below the selected value (last values)
percentage_below_last = (row_means_last.iloc[:, 0] <= selected_value_last).mean() * 100
percentage_below_last = round(percentage_below_last)  # Round to nearest whole number

st.write(f"Approximately **{percentage_below_last:.0f}%** of scenarios have a recent average amount of **${selected_value_last:,.0f}** or less.")

# Contextual explanation for last values
st.write(f"### What This Means for You in Recent Years")

st.markdown(f"""
Looking at the last **{number_of_last_columns} years**:

- There's about a **{percentage_below_last:.0f}%** chance that your average amount was **${selected_value_last:,.0f}** or less.
""")
