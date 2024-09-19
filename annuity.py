# Import necessary libraries
import streamlit as st
import pandas as pd

# Import Plotly for interactive plotting
import plotly.express as px

# Import ECDF from statsmodels
from statsmodels.distributions.empirical_distribution import ECDF

# Streamlit slider for number of years
number_of_years = st.slider("Select the number of years:", 1, 35, 30, step=1)

# Use number_of_years for the maximum_number_of_years_in_plan
maximum_number_of_years_in_plan = number_of_years

# Add a slider for the income amount
income_amount = st.slider(
    "Select the income amount:", 1000, 100000, 10000, step=1000
)

# Add a slider for the number of last values to consider
number_of_last_values = st.slider(
    "Select the number of last values to consider:", 1, number_of_years, 5, step=1
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

# **Adjust the data based on the selected income amount**
adjusted_data_df = cpi_isolated_data_df * income_amount

# Calculate the average of each row (full data corresponding to number_of_years)
row_means_full = (
    adjusted_data_df.mean(axis=1)
    .reset_index(drop=True)
    .to_frame(name="Mean of Full Data")
)

# Compute the mean, median, and minimum of the row means (full data)
mean_full = row_means_full["Mean of Full Data"].mean()
median_full = row_means_full["Mean of Full Data"].median()
min_full = row_means_full["Mean of Full Data"].min()

# Display the computed statistics (full data)
st.write("### Statistics of Row Means (Full Data)")
st.write(f"**Mean:** ${mean_full:,.0f}")
st.write(f"**Median:** ${median_full:,.0f}")
st.write(f"**Minimum:** ${min_full:,.0f}")

# **Add explanation for the ECDF chart**
st.write("### Understanding the ECDF Chart")
st.markdown("""
The **Empirical Cumulative Distribution Function (ECDF)** chart shows the proportion (or percentage) of data points that are less than or equal to a certain value.

In simple terms, the ECDF chart helps you understand how your data is distributed. It allows you to see:

- **At what value a certain percentage of the data lies below.**
- **What percentage of data falls below a particular value.**

For example, if you look at a point on the ECDF chart where the cumulative probability is **0.5** (or **50%**), the corresponding value on the x-axis tells you that **50% of the data points have a mean value less than or equal to that amount**.

This can help you answer questions like:

- *What is the value below which a certain percentage of outcomes fall?*
- *What is the likelihood that the mean value is less than a specific amount?*

By interpreting the ECDF chart, you can gain insights into the distribution of the mean values from your data, even without a statistical background.
""")

# Plot the ECDF of the row means (full data) using Plotly
st.write(
    "### Empirical Cumulative Distribution Function (ECDF) of Row Means (Full Data)"
)
fig_full = px.ecdf(
    row_means_full, 
    x="Mean of Full Data", 
    title="ECDF of Row Means (Full Data)",
    labels={"Mean of Full Data": "Mean Value ($)"},
)
st.plotly_chart(fig_full)

# **Updated Code for Last N Values Starts Here**

# Extract the last 'number_of_last_values' values from each row
number_of_columns = adjusted_data_df.shape[1]
number_of_last_columns = min(number_of_last_values, number_of_columns)
last_values_df = adjusted_data_df.iloc[:, -number_of_last_columns:]

# Calculate the mean of each row in the last values DataFrame
row_means_last = (
    last_values_df.mean(axis=1)
    .reset_index(drop=True)
    .to_frame(name=f"Mean of Last {number_of_last_columns} Values")
)

# Compute the mean, median, and minimum of the row means (last values)
mean_last = row_means_last.iloc[:, 0].mean()
median_last = row_means_last.iloc[:, 0].median()
min_last = row_means_last.iloc[:, 0].min()

# Display the computed statistics (last values)
st.write(
    f"### Statistics of Row Means (Last {number_of_last_columns} Values)"
)
st.write(f"**Mean:** ${mean_last:,.0f}")
st.write(f"**Median:** ${median_last:,.0f}")
st.write(f"**Minimum:** ${min_last:,.0f}")

# **Add explanation for the ECDF chart (Last Values)**
st.write(f"### Understanding the ECDF Chart for Last {number_of_last_columns} Values")
st.markdown(f"""
This ECDF chart represents the distribution of the mean values calculated from the **last {number_of_last_columns} values** of each row.

It helps you understand:

- **How the most recent data points are distributed.**
- **What percentage of recent data points fall below a certain value.**

By examining this chart, you can gain insights into recent trends or patterns in your data, which can be valuable for making predictions or informed decisions.
""")

# Plot the ECDF of the row means (last values) using Plotly
st.write(
    f"### Empirical Cumulative Distribution Function (ECDF) of Row Means (Last {number_of_last_columns} Values)"
)
fig_last = px.ecdf(
    row_means_last, 
    x=row_means_last.columns[0], 
    title=f"ECDF of Row Means (Last {number_of_last_columns} Values)",
    labels={row_means_last.columns[0]: "Mean Value ($)"},
)
st.plotly_chart(fig_last)