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

# **Dynamic explanation for the ECDF chart (Full Data)**
min_value_full = row_means_full["Mean of Full Data"].min()
max_value_full = row_means_full["Mean of Full Data"].max()
median_value_full = row_means_full["Mean of Full Data"].median()

st.write("### Explaining the ECDF Chart of Row Means (Full Data)")

# Explanation for the ECDF Chart (Full Data)
st.markdown(f"""
Let's explain this ECDF chart of Row Means (Full Data) using dollars.

### What This Chart Shows:
This chart gives a big picture of how much money different groups typically have, represented by the **average (mean) dollar amounts**.

### Reading the Chart:
- The **x-axis** shows dollar amounts ranging from ${min_value_full:,.0f} to ${max_value_full:,.0f}.
- The **y-axis** represents the proportion or percentage of groups we've counted so far.

### Understanding the Line:
- The line starts at the bottom left because no groups have been counted yet.
- As we move right, the line goes up, indicating we're counting more groups.
- By the time we reach the maximum value of ${max_value_full:,.0f}, we've counted almost all the groups (close to 100%).

### What We Can Learn:
- About half of the groups have average amounts below **${median_value_full:,.0f}**, as the line crosses the 50% mark at this value.
- Few groups have average amounts below **${min_value_full:,.0f}** or above **${max_value_full:,.0f}**.

### Example:
If you're interested in what percentage of groups have average amounts of $7,000 or less:
- Find $7,000 on the bottom of the chart.
- Look up to where the line intersects.
- The line at this point shows the cumulative proportion of groups whose average value is $7,000 or less.
""")

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

# **Dynamic explanation for the ECDF chart (Last N Values)**
min_value_last = row_means_last.iloc[:, 0].min()
max_value_last = row_means_last.iloc[:, 0].max()
median_value_last = row_means_last.iloc[:, 0].median()

st.write(f"### Explaining the ECDF Chart of Row Means (Last {number_of_last_columns} Values)")

# Explanation for the ECDF Chart (Last Values)
st.markdown(f"""
This ECDF chart represents the distribution of the **mean values** calculated from the last {number_of_last_columns} values of each row.

### What This Chart Shows:
This chart helps us understand recent trends in data, showing the distribution of recent average dollar amounts.

### Reading the Chart:
- The **x-axis** shows dollar amounts ranging from **${min_value_last:,.0f}** to **${max_value_last:,.0f}**.
- The **y-axis** shows the percentage of rows we've counted so far.

### Understanding the Line:
- The line starts at the bottom left because no rows have been counted yet.
- As we move to the right, the line goes up, indicating we're counting more rows.
- By the time we reach **${max_value_last:,.0f}**, we've counted almost all the rows (close to 100%).

### What We Can Learn:
- About half of the rows have average amounts below **${median_value_last:,.0f}**, as the line crosses the 50% mark here.
- Very few rows have average amounts below **${min_value_last:,.0f}** or above **${max_value_last:,.0f}**.

### Example:
If you're interested in knowing what percentage of rows have average amounts of $7,000 or less:
- Find $7,000 on the x-axis.
- Look up to where the line intersects.
- The line at that point shows the cumulative proportion of rows whose average value is $7,000 or less.
""")last)