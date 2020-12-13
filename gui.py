import streamlit as st


class FloatingKmGUI:
    def __init__(self):
        self.km_input = st.sidebar.number_input(
            label="Michaelis constant",
            min_value=1E-9,
            max_value=1.,
            value=42E-6,
            format="%.2e",
            step=1E-6
        )

        self.v_max_input = st.sidebar.number_input(
            label="Maximum reaction velocity",
            min_value=1E3,
            max_value=1E7,
            value=242E3,
            format="%.2e",
            step=1E3
        )

        self.max_concentration_input = st.sidebar.number_input(
            label="Maximum ATP concentration",
            min_value=1E-6,
            max_value=1E-3,
            value=1E-4,
            format="%.2e",
            step=1E-6
        )

        self.number_data_points_slider = st.sidebar.slider(
            "Number of data points",
            min_value=3,
            max_value=100,
            value=13,
            step=1
        )

        self.repetitions_slider = st.sidebar.slider(
            "Number of repetitions",
            min_value=1,
            max_value=10,
            value=3,
            step=1
        )

        self.relative_error_slider = st.sidebar.slider(
            "Relative error",
            min_value=1E-3,
            max_value=.999,
            value=.15,
            step=1E-3
        )

    def pyplot(self, fig):
        st.pyplot(fig)
