# Field trial simulation - V1
# guilherme borchardt - April, 2021
# simulation of inference about differences between averages.
# assumption: two independent variables that with similar variances and \
# follow normal distribution.
# inference statistics: T-Test for equal variance - two tails.


import numpy as np
from prettytable import PrettyTable
from scipy import stats
import matplotlib.pyplot as plt

# define the input parameters
###########################################################################################

product = 'XXXXX'
control_mean = 1.57  # mean currently  (e.g. no probiotic)
control_std_desv = .08  # standard deviation
treatment_mean = 1.6  # mean after treatment with product (e.g. with probiotic)
n_samples_per_treatment = 5  # number of samples (e.g. houses, litter, sows, etc)
n_trials_repetitions = 2  # number of repetitions to be simulated
p_level = .05  # decision level of the inference about the averages - Type I error

treatment_std_desv = control_std_desv  # consider standard deviation equal for both groups
#############################################################################################








def main():


    x = PrettyTable()
    print('\n@@@@ Field Trial Simulation @@@@\n')
    print('User inputted values\n')
    print(f'Control (no {product}) - {control_mean}')
    print(f'Treatment (with {product}) - {treatment_mean}\n')

    input('\npress Enter to continue...')

    print('Simulated trial results\n')
    x.field_names = ['trial run', 'n / treatment', 'Control - Average', f'{product} - Average', 'Delta of averages',
                     'Delta expected by customer?',
                     'AVGs comparison (TTest)', 'P', f'{product} Approved?']
    count_expected = 0
    diff_expected = 0

    for i in range(n_trials_repetitions):

        simul_data_control = np.random.normal(control_mean, control_std_desv, n_samples_per_treatment)
        simul_data_treatment = np.random.normal(treatment_mean, treatment_std_desv, n_samples_per_treatment)
        simul_control_average = round(np.average(simul_data_control), 3)
        simul_treatment_average = round(np.average(simul_data_treatment), 3)

        ttest, p = stats.ttest_ind(simul_data_control, simul_data_treatment)


        delta = round(simul_treatment_average - simul_control_average, 4)
        if p <= p_level:
            treat_accepted = 'YES'
            diff_expected = diff_expected + 1
        else:
            treat_accepted = '.'

        if treatment_mean < control_mean:
            if delta <= treatment_mean - control_mean:
                expected = 'YES'
                count_expected = count_expected + 1
            else:
                expected = '.'
        elif treatment_mean > control_mean:
            delta = round(simul_treatment_average - simul_control_average, 4)

            if delta >= treatment_mean - control_mean:
                expected = 'YES'
                count_expected = count_expected + 1
            else:
                expected = '.'
        else:
            print("verify your input")

        x.add_row([i + 1, n_samples_per_treatment, simul_control_average, simul_treatment_average, delta, expected,
                   round(ttest, 3), round(p, 3),
                   treat_accepted])

    print(str(x))

    trial_customer_expected = [n_trials_repetitions - count_expected, count_expected]
    trial_statistic_diff_expected = [n_trials_repetitions - diff_expected, diff_expected]

    if n_trials_repetitions >= 3:
        explode = [0, .05]
        plt.pie(trial_customer_expected,
                labels=['No', 'Yes'],
                startangle=90,
                autopct='%1.1f%%',
                colors=['red','green'],
                explode = explode,
                )
        plt.title(f'Will customer see some benefit of {product}?')
        plt.legend(loc='lower right')
        plt.show()

        plt.pie(trial_statistic_diff_expected,
                labels=['No', 'Yes'],
                startangle=90,
                autopct='%1.1f%%',
                colors=['red', 'green'],
                explode = explode,
                )
        plt.title(f'Will customer see a statistical significance between means using  {product}?')
        plt.legend(loc='lower right')

        plt.show()

    else:
        exit()



if __name__ ==  '__main__':
    main()
else:
    exit()






