# Import necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Streamlit app
def main():
    st.title('Chan plot [ Water Encroachment Analysis ]')

    # Step 1: File uploader for the Excel file
    uploaded_file = st.file_uploader("Upload your Excel file, Note: excel file should contain two columns days and readings ", type=["xlsx"])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)

        # Extracting days and readings
        days = df.iloc[:, 0].values  # Assuming the first column is days
        readings = df.iloc[:, 1].values  # Assuming the second column is readings

        # Inputs for the polynomial degrees
        degree_readings = st.number_input("Enter the degree of the polynomial for the WOR readings:", min_value=1, max_value=10, value=1)
        degree_derivative = st.number_input("Enter the degree of the polynomial for the WOR derivative:", min_value=1, max_value=10, value=1)

        # Checkbox to show/hide scatter points
        show_scatter = st.checkbox("Show scatter points", value=True)

        # Step 2: Plot the data
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if show_scatter:
            ax.scatter(days, readings, label='WOR', color='blue')

        # Set the x-axis to log scale
        ax.set_xscale('log')

        # Step 3: Calculate the derivative
        # Using numpy's gradient function to compute the numerical derivative
        derivative = np.gradient(readings, days)

        if show_scatter:
            # Step 4: Plot the derivative
            ax.scatter(days, derivative, label='WOR Derivative', color='red', linestyle='--')

        # Step 5: Calculate the best-fit polynomial for readings
        coeffs_readings = np.polyfit(np.log(days), readings, degree_readings)  # Log transform days for polynomial fit
        best_fit_poly_readings = np.polyval(coeffs_readings, np.log(days))

        # Plot the best-fit polynomial for readings
        ax.plot(days, best_fit_poly_readings, label=f'Best Fit Polynomial WOR over days (degree {degree_readings})', color='green')

        # Step 6: Calculate the best-fit polynomial for derivative
        coeffs_derivative = np.polyfit(np.log(days), derivative, degree_derivative)  # Log transform days for polynomial fit
        best_fit_poly_derivative = np.polyval(coeffs_derivative, np.log(days))

        # Plot the best-fit polynomial for derivative
        ax.plot(days, best_fit_poly_derivative, label=f'Best Fit Polynomial for WOR Derivative over days (degree {degree_derivative})', color='purple')

        # Adding titles and labels
        ax.set_title('Chan plot')
        ax.set_xlabel('Days (log scale)')
        ax.set_ylabel('WOR and WOR Derivative')
        ax.legend()
        ax.grid(True, which='both')

        # Show the plot
        st.pyplot(fig)

if __name__ == "__main__":
    main()
