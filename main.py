import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
import seaborn as sns
from statsmodels.distributions.empirical_distribution import ECDF

from gui import FloatingKmGUI
from simulation import get_kinetic_parameters_estimates

mpl.style.use("seaborn")

if __name__ == "__main__":
    floating_km_gui = FloatingKmGUI()
    v_max_estimates, k_m_estimates = get_kinetic_parameters_estimates(
                max_velocity=floating_km_gui.v_max_input,
                michaelis_constant=floating_km_gui.km_input,
                max_concentration=floating_km_gui.max_concentration_input,
                data_points_num=floating_km_gui.number_data_points_slider,
                relative_error=floating_km_gui.relative_error_slider,
                repetitions=floating_km_gui.repetitions_slider,
                simulations=1000
            )

    fig = plt.figure(figsize=(8, 8))

    plot_data = [
        ("Michaelis constant", k_m_estimates, floating_km_gui.km_input),
        ("Maximum velocity", v_max_estimates, floating_km_gui.v_max_input)
    ]

    for estimate_i, cur_data in enumerate(plot_data):
        estimate_title, estimate_data, estimate_input = cur_data
        ax = fig.add_subplot(2, 1, estimate_i + 1)
        ax.set_title(estimate_title)
        sns.kdeplot(estimate_data, ax=ax)

        line = ax.lines[0]
        kde_plot_xs = line.get_xdata()
        kde_plot_ys = line.get_ydata()

        y_min, y_max = ax.get_ylim()
        ecdf = ECDF(estimate_data)

        for range_i in range(3, 0, -1):
            lower_bound = estimate_input * (1 - range_i / 10)
            upper_bound = estimate_input * (1 + range_i / 10)
            auc = ecdf([upper_bound])[0] - ecdf([lower_bound])[0]

            begin = np.argmin(np.abs(lower_bound - kde_plot_xs))
            end = np.argmin(np.abs(upper_bound - kde_plot_xs))

            polygon_points = [(kde_plot_xs[begin], 0)] +\
                list(zip(kde_plot_xs[begin:end], kde_plot_ys[begin:end])) +\
                [(kde_plot_xs[end-1], 0)]
            polygon_points = np.array(polygon_points)
            poly = Polygon(polygon_points,
                           facecolor=f"C{range_i}",
                           edgecolor="0.5",
                           alpha=.6,
                           label=f"± {range_i}0%: {auc*100:.1f}%"
                           )
            ax.add_patch(poly)
            ax.legend()

    floating_km_gui.pyplot(fig)
