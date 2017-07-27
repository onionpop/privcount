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
# assume 1 circuit can handle all requests
sensitivity_circuits = 6*8+10

# protect 1 site per 10 minutes for 1 hour
# according to marc's crawler results, 75% of crawled sites use 4 or fewer circuits
# each client-created circuit results in a rend_c and a rend_s circuits
sensitivity_rend_c_circuits = 6*1*4
# protect a rend_s for each rend_c circuit
sensitivity_rend_s_circuits = sensitivity_rend_c_circuits
sensitivity_rend_circuits = sensitivity_rend_c_circuits + sensitivity_rend_s_circuits

# 2 facebook logins per day
# 75% of facebook crawls use 8 or fewer circuits according to marc's crawler results
# assume persistent connections
sensitivity_fb_circuits = 2*8

# we don't need to protect circuits that our crawler creates
sensitivity_crawler_circuits = 0

##### estimated values #####

# taken from p2p initial data collection 6/16/16-6/17/16
num_circuits_per_day = 8131540.0/2

# estimate based on metrics: hs is 1% of all traffic by bytes
num_rend_c_circuits_per_day = num_circuits_per_day * 0.01
num_rend_s_circuits_per_day = num_rend_c_circuits_per_day
num_rend_circuits_per_day = num_rend_c_circuits_per_day + num_rend_s_circuits_per_day

# estimate that facebook is 25% of all client usage
num_fb_circuits_per_day = num_rend_c_circuits_per_day * 0.25

# set crawler values to 0 so noise script works correctly
num_crawler_circuits_per_day = 0

##### parameters that will be re-used #####

circuit_parameters = (sensitivity_circuits * epoch_length_days, num_circuits_per_day * epoch_length_days)
circuit_rend_c_parameters = (sensitivity_rend_c_circuits * epoch_length_days, num_rend_c_circuits_per_day * epoch_length_days)
circuit_rend_s_parameters = (sensitivity_rend_s_circuits * epoch_length_days, num_rend_s_circuits_per_day * epoch_length_days)
circuit_rend_parameters = (sensitivity_rend_circuits * epoch_length_days, num_rend_circuits_per_day * epoch_length_days)
circuit_fb_parameters = (sensitivity_fb_circuits * epoch_length_days, num_fb_circuits_per_day * epoch_length_days)
circuit_crawler_parameters = (sensitivity_crawler_circuits * epoch_length_days, num_crawler_circuits_per_day * epoch_length_days)

# these are all "single counter" type of statistics
# for a list of all classification-related counters, see doc/ClassificationCounters.markdown
onionpop_parameters = {
    # normal circuit counters
    'MidCircuitCount': circuit_parameters,
    'EntryCircuitCount': circuit_parameters,
    'EndCircuitCount': circuit_parameters,

    # hs-related circuit counters
    'Rend2CircuitCount': circuit_rend_parameters,
    'Rend2MultiHopClientCircuitCount': circuit_rend_parameters,
    'Rend2ClientCircuitCount': circuit_rend_c_parameters,
    'Rend2ServiceCircuitCount': circuit_rend_s_parameters,
    'ExitAndRend2ClientCircuitCount': circuit_parameters,
    'ExitAndRend2ServiceCircuitCount': circuit_parameters,
    'Rend2SingleOnionServiceFacebookASNCircuitCount': circuit_fb_parameters,

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

if __name__ == '__main__':
    epsilon = 0.3
    delta = 1e-3
    excess_noise_ratio = num_relay_machines # factor by which noise is expanded to allow for malicious relays
    sigma_tol = psn.DEFAULT_SIGMA_TOLERANCE
    epsilon_tol = psn.DEFAULT_EPSILON_TOLERANCE
    sigma_ratio_tol = psn.DEFAULT_SIGMA_RATIO_TOLERANCE

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
                                   sanity_check=None)

    # add single bins, that way we can use the resulting output as both the noise
    # file and the bins file.
    if 'counters' in noise_parameters:
        for param in noise_parameters['counters']:
            noise_parameters['counters'][param]['bins'] = [[float('-inf'), float('inf')]]

    #print('onionpop noise config\n-----')
    print yaml.dump(noise_parameters, default_flow_style=False)
