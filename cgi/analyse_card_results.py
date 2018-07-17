from __future__ import division
__author__ = 's1005849'

from enum import Enum
import numpy as np
import scipy.stats as stats
import extract_data
import survey_results
import matplotlib.pyplot as plt


def mean(values):
    return np.mean(values)


def std_error_on_mean(values):
    return stats.sem(values)

def std_dev(values):
    return np.std(values)

def var(values):
    return np.var(values)


class Criteria(Enum):
    multiple = 1
    sum = 2
    card = 3

class Direction(Enum):
    smallest = 1
    biggest = 2

def number_trials(trials):
    numbered_trials = {}
    for i in range(1, 11):
        numbered_trials[i] = [t for t in trials if len(t['cardsFlipped']) > 0 and
                              t['cards'][t['cardsFlipped'][0]]['value'] == i]
    return numbered_trials

def split_trials_by_criteria(trials):
    split_trials = {
                    Criteria.multiple: [t for t in trials if t['criteria'] == 'Multiple'] }
    return split_trials

def split_trials_by_direction(trials):
    split_trials = {Direction.biggest: [t for t in trials if t['direction'] == 'Biggest'],
                    Direction.smallest: [t for t in trials if t['direction'] == 'Smallest']}
    return split_trials

def only_guessed_trials(trials):
    return [t for t in trials if len(t['cardsFlipped']) == 1]

def split_trials_by_type(trials):
    return {'AA': [t for t in trials if t['trialType'] == 'AA'], 'AB': [t for t in trials if t['trialType'] == 'AB']}

def calculate_probability_a_guessed(trials):
    if len(trials) == 0:
        return None
    guessed_a_list = []
    for t in trials:
        cards_flipped = t['cardsFlipped']
        if (((cards_flipped[0] == 0 or cards_flipped[0] == 1) and (t['guessMade'] == 'T')) or
                ((cards_flipped[0] == 2 or cards_flipped[0] == 3) and (t['guessMade'] == 'B'))):
            guessed_a_list.append(1)
        else:
            guessed_a_list.append(0)
    guessed_a_array = np.asarray(guessed_a_list)
    value = mean(guessed_a_array)
    sd = std_error_on_mean(guessed_a_array)
    variance = sd**2
    return {'value': value, 'sd': sd, 'variance': variance}

def arrange_trials_for_ruo_bias(trials):
    split_trials = split_and_number_trials(trials)
    for k1 in split_trials.keys():
        for k2 in split_trials[k1].keys():
            for k3, v3 in split_trials[k1][k2].items():
                guessed_trials = only_guessed_trials(v3)
                split_trials[k1][k2][k3] = split_trials_by_type(guessed_trials)
    return split_trials



def split_and_number_trials(trials):
    split_trials = split_trials_by_criteria(trials)
    for k1, v1 in split_trials.items():
        split_trials[k1] = split_trials_by_direction(v1)
        for k2, v2 in split_trials[k1].items():
            split_trials[k1][k2] = number_trials(v2)
    return split_trials

def calculate_probability(arranged_trials, criteria, direction, i):
    trial_guessed_arr = np.asarray([int(len(t['cardsFlipped']) == 1) for t in arranged_trials[criteria][direction][i]])
    value = mean(trial_guessed_arr)
    sd = std_error_on_mean(trial_guessed_arr)
    variance = sd**2
    return {'value': value, 'sd': sd, 'variance': variance}

def probability_of_guessing(trials):
    trial_guessed_arr = np.asarray([int(len(t['cardsFlipped']) == 1) for t in trials])
    return mean(trial_guessed_arr)

def calculate_ruo_bias(trials_arranged_for_ruo_bias, criteria, direction):
    summary_stat = 0.0
    for i in range(1, 11):
        aa_trials = trials_arranged_for_ruo_bias[criteria][direction][i]['AA']
        ab_trials = trials_arranged_for_ruo_bias[criteria][direction][i]['AB']
        if len(aa_trials) == 0 or len(ab_trials) == 0:
            continue
        aa_prob = calculate_probability_a_guessed(aa_trials)['value']
        ab_prob = calculate_probability_a_guessed(ab_trials)['value']
        summary_stat += (ab_prob - aa_prob)

    return summary_stat


def calculate_pea_bias(arranged_trials, criteria):
    '''
    Function for calculating positive evidence approach bias.

    :param arranged_trials: Trials arranged by criteria, direction and first card value.
    :param criteria: Criteria to calculate bias for (Multiple or Sum)
    :return: Dictionary containing keys giving the value and various statistical properties
    '''
    biggest_sub_keys = [1, 2, 3, 4, 5]
    smallest_sub_keys = [6, 7, 8, 9, 10]
    summary_stat = 0.0

    for i in range(1, 11):
        if ((len(arranged_trials[criteria][Direction.biggest][i]) == 0)
                or (len(arranged_trials[criteria][Direction.smallest][i]) == 0)):
            continue

        prob = calculate_probability(arranged_trials, criteria, Direction.biggest, i)
        if i in biggest_sub_keys:
            part = -prob['value']
        else:
            part = prob['value']
        summary_stat += part

        prob = calculate_probability(arranged_trials, criteria, Direction.smallest, i)
        if i in smallest_sub_keys:
            part = -prob['value']
        else:
            part = prob['value']
        summary_stat += part

    return summary_stat




participant_choices = extract_data.retrieve_game_choices()
pea_mult_for_avg = []
pea_mult_for_reg = []
prob_for_avg = []
prob_for_reg = []
ruo_mult_for_avg = []
ruo_mult_for_reg = []
coins_list = []
max_coins = 0
for i, trials in enumerate(participant_choices):
    if trials is None:
        pea_mult_for_reg.append(None)
        prob_for_reg.append(None)
        continue
    arranged_trials = split_and_number_trials(trials)
    ruo_arranged_trials = arrange_trials_for_ruo_bias(trials)
    prob = probability_of_guessing(trials)
    pea_mult = calculate_pea_bias(arranged_trials, Criteria.multiple)
    ruo_mult = calculate_ruo_bias(ruo_arranged_trials, Criteria.multiple, Direction.biggest)
    if pea_mult is not None:
        pea_mult_for_avg.append(pea_mult)
    if ruo_mult is not None:
        ruo_mult_for_avg.append(ruo_mult)
    pea_mult_for_reg.append(pea_mult)
    prob_for_reg.append(prob)
    prob_for_avg.append(prob)
    ruo_mult_for_reg.append(ruo_mult)
    coins = trials[-1]['coins']
    coins_list.append(coins)
    if coins > max_coins:
        max_coins = coins
    print 'Participant: ', i
    print 'Positive Evidence Approach: ', pea_mult
    print 'Rejecting Unsampled Options: ', ruo_mult
    print 'Coins: ', trials[-1]['coins']

print 'Winning Coins: ', max_coins
print 'Average Positive Evidence Approach: ', mean(pea_mult_for_avg)
print 'Standard Error on Mean Positive Evidence Approach: ', std_error_on_mean(pea_mult_for_avg)
print 'Standard Deviation Positive Evidence Approach:  ', std_dev(pea_mult_for_avg)
print
print 'Average Rejecting Unsampled Options: ', mean(ruo_mult_for_avg)
print 'Standard Error on Mean Rejecting Unsampled Options: ', std_error_on_mean(ruo_mult_for_avg)
print 'Standard Deviation Positive Evidence Approach:  ', std_dev(ruo_mult_for_avg)
print
all_trials = extract_data.all_game_choices()
ruo_all_trials_arrangement = arrange_trials_for_ruo_bias(all_trials)
pea_all_trails_arrangement = split_and_number_trials(all_trials)
pea_bias = calculate_pea_bias(pea_all_trails_arrangement, Criteria.multiple)
ruo_bias = calculate_ruo_bias(ruo_all_trials_arrangement, Criteria.multiple, Direction.smallest)
print 'Total Rejecting Unsampled Options Bias: ', ruo_bias
print 'Total Positive Evidence Approach Bias: ', pea_bias

raw_optimism = survey_results.get_survey_dict()[18]
raw_phq = survey_results.get_survey_dict()[21]
raw_altman = survey_results.get_survey_dict()[20]
raw_spq = survey_results.get_survey_dict()[19]
optimism_results = [result for i, result in enumerate(raw_optimism) if pea_mult_for_reg[i] is not None]
phq_results = [result for i, result in enumerate(raw_phq) if pea_mult_for_reg[i] is not None]
altman_results = [result for i, result in enumerate(raw_altman) if pea_mult_for_reg[i] is not None]
spq_results = [result for i, result in enumerate(raw_spq) if pea_mult_for_reg[i] is not None]

print 'Coin Correlations'
print
print 'Optimism Correlation Coefficient: ', np.corrcoef(optimism_results, coins_list)[0][1]
print 'PHQ-9 Correlation Coefficient: ', np.corrcoef(phq_results, coins_list)[0][1]
print 'Altman Correlation Coefficient: ', np.corrcoef(altman_results, coins_list)[0][1]
print 'SPQ Correlation Coefficient: ', np.corrcoef(spq_results, coins_list)[0][1]
print
print 'Spearman Correlations'
print 'Optimism Correlation Coefficient: ', stats.spearmanr(optimism_results, coins_list)
print 'PHQ-9 Correlation Coefficient: ', stats.spearmanr(phq_results, coins_list)
print 'Altman Correlation Coefficient: ', stats.spearmanr(altman_results, coins_list)
print 'SPQ Correlation Coefficient: ', stats.spearmanr(spq_results, coins_list)
print
print
print 'Positive Evidence Approach Correlations'
print
print 'Optimism Correlation Coefficient: ', np.corrcoef(optimism_results, pea_mult_for_avg)[0][1]
print 'PHQ-9 Correlation Coefficient: ', np.corrcoef(phq_results, pea_mult_for_avg)[0][1]
print 'Altman Correlation Coefficient: ', np.corrcoef(altman_results, pea_mult_for_avg)[0][1]
print 'SPQ Correlation Coefficient: ', np.corrcoef(spq_results, pea_mult_for_avg)[0][1]
print
print 'Spearman Correlations'
print 'Optimism Correlation Coefficient: ', stats.spearmanr(optimism_results, pea_mult_for_avg)
print 'PHQ-9 Correlation Coefficient: ', stats.spearmanr(phq_results, pea_mult_for_avg)
print 'Altman Correlation Coefficient: ', stats.spearmanr(altman_results, pea_mult_for_avg)
print 'SPQ Correlation Coefficient: ', stats.spearmanr(spq_results, pea_mult_for_avg)
print

print 'Kendall Tau Correlations'
print 'Optimism Correlation Coefficient: ', stats.kendalltau(optimism_results, pea_mult_for_avg)
print 'PHQ-9 Correlation Coefficient: ', stats.kendalltau(phq_results, pea_mult_for_avg)
print 'Altman Correlation Coefficient: ', stats.kendalltau(altman_results, pea_mult_for_avg)
print 'SPQ Correlation Coefficient: ', stats.kendalltau(spq_results, pea_mult_for_avg)
print


plt.figure(0)
plt.hist(coins_list)
plt.xlabel('Coins')
plt.yticks(range(21))

plt.figure(1)
plt.scatter(optimism_results, pea_mult_for_avg)
plt.xlabel('Optimism Score (LOTR)')
plt.ylabel('Positive Evidence Approach')

plt.figure(2)
plt.scatter(phq_results, pea_mult_for_avg)
plt.xlabel('PHQ')
plt.ylabel('Positive Evidence Approach')

plt.figure(3)
plt.scatter(altman_results, pea_mult_for_avg)
plt.xlabel('Altman')
plt.ylabel('Positive Evidence Approach')


plt.figure(4)
plt.scatter(spq_results, pea_mult_for_avg)
plt.xlabel('SPQ')
plt.ylabel('Positive Evidence Approach')



print 'Guessing Probability Correlations'
print
optimism_results = [result for i, result in enumerate(raw_optimism) if prob_for_reg[i] is not None]
phq_results = [result for i, result in enumerate(raw_phq) if prob_for_reg[i] is not None]
altman_results = [result for i, result in enumerate(raw_altman) if prob_for_reg[i] is not None]
spq_results = [result for i, result in enumerate(raw_spq) if prob_for_reg[i] is not None]
print 'Optimism Correlation Coefficient: ', np.corrcoef(optimism_results, prob_for_avg)[0][1]
print 'PHQ-9 Correlation Coefficient: ', np.corrcoef(phq_results, prob_for_avg)[0][1]
print 'Altman Correlation Coefficient: ', np.corrcoef(altman_results, prob_for_avg)[0][1]
print 'SPQ Correlation Coefficient: ', np.corrcoef(spq_results, prob_for_avg)[0][1]
print
print 'Spearman Correlations'
print 'Optimism Correlation Coefficient: ', stats.spearmanr(optimism_results, prob_for_avg)
print 'PHQ-9 Correlation Coefficient: ', stats.spearmanr(phq_results, prob_for_avg)
print 'Altman Correlation Coefficient: ', stats.spearmanr(altman_results, prob_for_avg)
print 'SPQ Correlation Coefficient: ', stats.spearmanr(spq_results, prob_for_avg)
print
print 'Kendall Tau Correlations'
print 'Optimism Correlation Coefficient: ', stats.kendalltau(optimism_results, prob_for_avg)
print 'PHQ-9 Correlation Coefficient: ', stats.kendalltau(phq_results, prob_for_avg)
print 'Altman Correlation Coefficient: ', stats.kendalltau(altman_results, prob_for_avg)
print 'SPQ Correlation Coefficient: ', stats.kendalltau(spq_results, prob_for_avg)
print

plt.figure(5)
plt.scatter(optimism_results, prob_for_avg)
plt.xlabel('Optimism Score (LOTR)')
plt.ylabel('Probability of Guessing')


plt.figure(6)
plt.scatter(phq_results, prob_for_avg)
plt.xlabel('PHQ')
plt.ylabel('Probability of Guessing')


plt.figure(7)
plt.scatter(altman_results, prob_for_avg)
plt.xlabel('Altman')
plt.ylabel('Probability of Guessing')

plt.figure(8)
plt.scatter(spq_results, prob_for_avg)
plt.xlabel('SPQ')
plt.ylabel('Probability of Guessing')



print 'Intersurvey Correlations'
print
print 'Depression Mania Correlation: ', np.corrcoef(raw_phq, raw_altman)[0][1]
print 'Depression Optimism Correlation: ', np.corrcoef(raw_phq, raw_optimism)[0][1]
print 'Depression SPQ Correlation: ', np.corrcoef(raw_phq, raw_spq)[0][1]
print 'Optimism Mania Correlation: ', np.corrcoef(raw_optimism, raw_altman)[0][1]
print 'Mania SPQ Correlation: ', np.corrcoef(raw_altman, raw_spq)[0][1]
print
print 'Spearman Correlations'
print 'Depression Mania Correlation: ', stats.spearmanr(raw_phq, raw_altman)
print 'Depression Optimism Correlation: ', stats.spearmanr(raw_phq, raw_optimism)
print 'Depression SPQ Correlation: ', stats.spearmanr(raw_phq, raw_spq)
print 'Optimism Mania Correlation: ', stats.spearmanr(raw_optimism, raw_altman)
print 'Mania SPQ Correlation: ', stats.spearmanr(raw_altman, raw_spq)
print
print 'Kendall Tau Correlations'
print 'Depression Mania Correlation: ', stats.kendalltau(raw_phq, raw_altman)
print 'Depression Optimism Correlation: ', stats.kendalltau(raw_phq, raw_optimism)
print 'Depression SPQ Correlation: ', stats.kendalltau(raw_phq, raw_spq)
print 'Optimism Mania Correlation: ', stats.kendalltau(raw_optimism, raw_altman)
print 'Mania SPQ Correlation: ', stats.kendalltau(raw_altman, raw_spq)



plt.figure(9)
plt.scatter(raw_phq, raw_altman)
plt.xlabel('PHQ')
plt.ylabel('Altman')


plt.figure(10)
plt.scatter(raw_phq, raw_optimism)
plt.xlabel('PHQ')
plt.ylabel('Optimism (LOTR)')


plt.figure(11)
plt.scatter(raw_phq, raw_spq)
plt.xlabel('PHQ')
plt.ylabel('SPQ')

plt.figure(12)
plt.scatter(raw_optimism, raw_altman)
plt.xlabel('Optimism')
plt.ylabel('Altman')

plt.figure(13)
plt.scatter(raw_altman, raw_spq)
plt.xlabel('Mania')
plt.ylabel('SPQ')


prob_biggest = [calculate_probability(pea_all_trails_arrangement, Criteria.multiple, Direction.biggest, i)['value'] for i in range(1, 11)]
prob_smallest = [calculate_probability(pea_all_trails_arrangement, Criteria.multiple, Direction.smallest, i)['value'] for i in range(1, 11)]
plt.figure(14)
plt.scatter(range(1,11), prob_biggest)
plt.scatter(range(1,11), prob_smallest)
plt.legend(['biggest', 'smallest'])
plt.xlabel('Number')
plt.ylabel('Probability')

plt.show()

