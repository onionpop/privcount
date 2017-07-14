# See LICENSE for licensing information

import math
import yaml

import privcount.statistics_noise as psn

## useful constants
NUM_SECONDS_PER_DAY = 24*60*60
NUM_MICROSECONDS_PER_SECOND = 1000*1000
NUM_MICROSECONDS_PER_DAY = NUM_SECONDS_PER_DAY * NUM_MICROSECONDS_PER_SECOND

## measurement parameters ##
epoch_length_days = 1.0 # length of collection round in days
epoch_length_seconds = epoch_length_days * NUM_SECONDS_PER_DAY
epoch_length_microseconds = epoch_length_days * NUM_MICROSECONDS_PER_DAY
slice_length_seconds = 10*60 # time slice for sensitive data in seconds
slice_length_microseconds = slice_length_seconds * NUM_MICROSECONDS_PER_SECOND
num_relay_machines = 3 # number of 'compromises' we protect against

##### privacy sensitivity #####

# protect 1 site per 10 minutes for 8 hours (plus other circuits)
sensitivity_circuits = 6*8+10

# protect 1 site per 10 minutes for 1 hour; each results in 4 rend_c and 4 rend_s circuits
sensitivity_rend_c_circuits = 6*1*4
# protect a rend_s for each rend_c circuit
sensitivity_rend_s_circuits = sensitivity_rend_c_circuits
sensitivity_rend_circuits = sensitivity_rend_c_circuits + sensitivity_rend_s_circuits

# 2 facebook logins per day (assume each session results in a long-lived persistent connection)
sensitivity_fb_circuits = 2

# we don't need to protect circuits that our crawler creates
sensitivity_crawler_circuits = 1 # use 1 instead of 0 to avoid corner case error in noise script

##### estimated values #####

# taken from p2p initial data collection 6/16/16-6/17/16
num_circuits_per_day = 8131540.0/2

# guessed based on metrics: hs is 1% of all traffic by bytes
num_rend_c_circuits_per_day = num_circuits_per_day * 0.01
num_rend_s_circuits_per_day = num_rend_c_circuits_per_day
num_rend_circuits_per_day = num_rend_c_circuits_per_day + num_rend_s_circuits_per_day

# facebook is 25% of all client usage
num_fb_circuits_per_day = num_rend_c_circuits_per_day * 0.25

# based on crawler schedule
num_crawler_circuits_per_day = 24*60

##### parameters that will be re-used #####

circuit_parameters = (sensitivity_circuits * epoch_length_days, num_circuits_per_day * epoch_length_days)
circuit_rend_c_parameters = (sensitivity_rend_c_circuits * epoch_length_days, num_rend_c_circuits_per_day * epoch_length_days)
circuit_rend_s_parameters = (sensitivity_rend_s_circuits * epoch_length_days, num_rend_s_circuits_per_day * epoch_length_days)
circuit_rend_parameters = (sensitivity_rend_circuits * epoch_length_days, num_rend_circuits_per_day * epoch_length_days)
circuit_fb_parameters = (sensitivity_fb_circuits * epoch_length_days, num_fb_circuits_per_day * epoch_length_days)
circuit_crawler_parameters = (sensitivity_crawler_circuits * epoch_length_days, num_crawler_circuits_per_day * epoch_length_days)

# these are all "single counter" type of statistics
onionpop_parameters = {
    # normal circuit counters
    'MidCircuitCount': circuit_parameters,
    'EntryCircuitCount': circuit_parameters,
    'EndCircuitCount': circuit_parameters,

    # hs-related circuit counters
    'RendCircuitCount': circuit_rend_parameters,
    'RendMultiHopClientCircuitCount': circuit_rend_parameters,
    'RendClientCircuitCount': circuit_rend_c_parameters,
    'RendServiceCircuitCount': circuit_rend_s_parameters,
    'ExitAndRendClientCircuitCount': circuit_parameters,
    'ExitAndRendServiceCircuitCount': circuit_parameters,
    'RendSingleOnionServiceFacebookASNCircuitCount': circuit_fb_parameters,

    # classficiation counters
    # hidden service protocol popularity
    'MidNoSignalPredictPurposeCircuitCount': circuit_parameters,
    'MidNoSignalPredictRendPurposeCircuitCount': circuit_rend_parameters,
    'MidNoSignalPredictNotRendPurposeCircuitCount': circuit_parameters, # could optimize?

    'MidGotSignalPredictPurposeCircuitCount': circuit_crawler_parameters,
    'MidGotSignalPredictRendPurposeCircuitCount': circuit_crawler_parameters,
    'MidGotSignalPredictNotRendPurposeCircuitCount': circuit_crawler_parameters,

    # GCM position
    'MidNoSignalPredictRendPurposePredictCGMPositionCircuitCount': circuit_rend_c_parameters, # could optimize?
    'MidNoSignalPredictRendPurposePredictNotCGMPositionCircuitCount': circuit_rend_parameters, # could optimize?

    'MidGotSignalPredictRendPurposePredictCGMPositionCircuitCount': circuit_crawler_parameters,
    'MidGotSignalPredictRendPurposePredictNotCGMPositionCircuitCount': circuit_crawler_parameters,

    # facebook webpage
    'MidNoSignalPredictRendPurposePredictCGMPositionPredictFBSiteCircuitCount': circuit_fb_parameters,
    'MidNoSignalPredictRendPurposePredictCGMPositionPredictNotFBSiteCircuitCount': circuit_rend_c_parameters, # could optimize?

    'MidGotSignalPredictRendPurposePredictCGMPositionPredictFBSiteCircuitCount': circuit_crawler_parameters,
    'MidGotSignalPredictRendPurposePredictCGMPositionPredictNotFBSiteCircuitCount': circuit_crawler_parameters,
}

''' list of all classification-specific counters, for reference
    'MidPredictPurposeCircuitCount': circuit_parameters,
    'MidGotSignalPredictPurposeCircuitCount': circuit_parameters,
    'MidNoSignalPredictPurposeCircuitCount': circuit_parameters,
    'MidPredictRendPurposeCircuitCount': circuit_parameters,
    'MidGotSignalPredictRendPurposeCircuitCount': circuit_parameters,
    'MidNoSignalPredictRendPurposeCircuitCount': circuit_parameters,
    'MidPredictNotRendPurposeCircuitCount': circuit_parameters,
    'MidGotSignalPredictNotRendPurposeCircuitCount': circuit_parameters,
    'MidNoSignalPredictNotRendPurposeCircuitCount': circuit_parameters,
    'MidPredictRendPurposePredictCGMPositionCircuitCount': circuit_parameters,
    'MidGotSignalPredictRendPurposePredictCGMPositionCircuitCount': circuit_parameters,
    'MidNoSignalPredictRendPurposePredictCGMPositionCircuitCount': circuit_parameters,
    'MidPredictRendPurposePredictNotCGMPositionCircuitCount': circuit_parameters,
    'MidGotSignalPredictRendPurposePredictNotCGMPositionCircuitCount': circuit_parameters,
    'MidNoSignalPredictRendPurposePredictNotCGMPositionCircuitCount': circuit_parameters,
    'MidPredictRendPurposePredictCGMPositionPredictFBSiteCircuitCount': circuit_parameters,
    'MidGotSignalPredictRendPurposePredictCGMPositionPredictFBSiteCircuitCount': circuit_parameters,
    'MidNoSignalPredictRendPurposePredictCGMPositionPredictFBSiteCircuitCount': circuit_parameters,
    'MidPredictRendPurposePredictCGMPositionPredictNotFBSiteCircuitCount': circuit_parameters,
    'MidGotSignalPredictRendPurposePredictCGMPositionPredictNotFBSiteCircuitCount': circuit_parameters,
    'MidNoSignalPredictRendPurposePredictCGMPositionPredictNotFBSiteCircuitCount': circuit_parameters,
'''

if __name__ == '__main__':
    epsilon = 0.3
    delta = 1e-3
    excess_noise_ratio = num_relay_machines # factor by which noise is expanded to allow for malicious relays
    sigma_tol = psn.DEFAULT_SIGMA_TOLERANCE
    epsilon_tol = psn.DEFAULT_EPSILON_TOLERANCE
    sigma_ratio_tol = psn.DEFAULT_SIGMA_RATIO_TOLERANCE

    # get optimal noise allocation for initial statistics
    (epsilons, sigmas, sigma_ratio) =  psn.get_opt_privacy_allocation(epsilon,
        delta, onionpop_parameters, excess_noise_ratio, sigma_tol=sigma_tol,
        epsilon_tol=epsilon_tol, sigma_ratio_tol=sigma_ratio_tol)

    # print information about traffic model statistics noise
    #print('\n* Classifier stats *\n')
    #psn.print_privacy_allocation(onionpop_parameters, sigmas, epsilons, excess_noise_ratio)

    psn.compare_noise_allocation(epsilon, delta, onionpop_parameters,
                             excess_noise_ratio,
                             sigma_tol=sigma_tol,
                             epsilon_tol=epsilon_tol,
                             sigma_ratio_tol=sigma_ratio_tol,
                             sanity_check=psn.DEFAULT_DUMMY_COUNTER_NAME)

    noise_parameters =\
        psn.get_noise_allocation_stats(epsilon, delta, onionpop_parameters,
                                   excess_noise_ratio,
                                   sigma_tol=sigma_tol,
                                   epsilon_tol=epsilon_tol,
                                   sigma_ratio_tol=sigma_ratio_tol,
                                   sanity_check=psn.DEFAULT_DUMMY_COUNTER_NAME)

    # add single bins, that way we can use the resulting output as both the noise
    # file and the bins file.
    if 'counters' in noise_parameters:
        for param in noise_parameters['counters']:
            noise_parameters['counters'][param]['bins'] = [[float('-inf'), float('inf')]]

    #print('onionpop noise config\n-----')
    print yaml.dump(noise_parameters, default_flow_style=False)
