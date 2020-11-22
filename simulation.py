import numpy as np
from scipy.optimize import minimize


def get_kinetic_parameters_estimates(
        max_velocity: float,
        michaelis_constant: float,
        max_concentration: float,
        data_points_num: int,
        relative_error: float,
        repetitions: int,
        simulations: int
) -> ([float], [float]):
    # Returns samples of K_m and V_max
    min_concentration = max_concentration / 2 ** (data_points_num - 1)
    substrate_concentrations = np.logspace(np.log2(min_concentration),
                                           max_concentration,
                                           num=data_points_num,
                                           base=2
                                           )

    # y = V_max * S / (K_m + S)
    y = max_velocity * substrate_concentrations / (michaelis_constant + substrate_concentrations)

    def loss(params):
        v_max, k_m = params
        s = substrate_concentrations
        return np.sum(np.power((y + y_err) - (v_max * s / (k_m + s)), 2))

    v_max_estimates = []
    k_m_estimates = []

    for _ in range(simulations):
        # measurement errors
        y_err = np.random.randn(*y.shape, repetitions).mean(axis=1) * y * relative_error

        res = minimize(fun=loss,
                       x0=np.array([1e5, 1e-4]),
                       method="Nelder-Mead")

        k_m_estimates.append(res.x[1])
        v_max_estimates.append(res.x[0])

    return v_max_estimates, k_m_estimates
