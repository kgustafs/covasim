'''
Simple script for running Covasim scenarios
'''

import sciris as sc
import covasim as cv


sc.heading('Setting up...')

# Run options
do_run  = 1
do_save = 0 # refers to whether to save plot - see also save_sims
do_plot = 1
do_show = 1
verbose = 1

dayptest1 = 13

# Sim options
#interv_day = 14
interv_eff = 0.7
#default_beta = 0.015 # Should match parameters.py

basepars = {
  'pop_size': 338,
  'pop_type': 'random',
  'start_day': '2020-04-09',
  'n_imports': 0,
  'pop_infected': 1
  }

metapars = {
  'n_runs': 3, # Number of parallel runs; change to 3 for quick, 11 for real
  'noise': 0.1, # Use noise, optionally
  'noisepar': 'beta',
  'rand_seed': 1,
  'quantiles': {'low':0.1, 'high':0.9},
  }

# For saving
version  = 'v0'
date     = '2020mar24'
folder   = 'results'
basename = f'{folder}/covasim_scenarios_{date}_{version}'
fig_path = f'{basename}.png'
obj_path = f'{basename}.scens'

# Define the scenarios
scenarios = {
#    'baseline': {
#        'name':'Baseline',
#        'pars': {
#        'interventions': None,
#        }
#    },
    'test': { #isolate positive tests
        'name':'50/10 test',
        'pars': {
        'interventions': cv.test_prob(symp_prob=0.5, asymp_prob=0.1, symp_quar_prob=1, asymp_quar_prob=1, loss_prob=0, test_delay=3,start_day=dayptest1)
        }
    },
   'PPEtest': {
       'name':'PPE and 50/10 test',
       'pars': {
       'interventions': [cv.change_beta(days=dayptest1, changes=interv_eff),
        cv.test_prob(symp_prob=0.5, asymp_prob=0.1, symp_quar_prob=1, asymp_quar_prob=0.1, loss_prob=0, test_delay=3,start_day=dayptest1)]
       }
    },
#            'distance2': { # With noise = 0.0, this should be identical to the above
#             'name':'Social distancing, version 2',
#              'pars': {
#                  'interventions': cv.dynamic_pars({'beta':dict(days=interv_day, vals=interv_eff*default_beta)})
#                  }
#              },
#    'lowtesttrace': { #isolate positive tests
#        'name':'PPE, 50/10 test, and ROM',
#        'pars': {
#            'quar_eff': {'a': 0.1},
#            'quar_period': 14,
#            'interventions': [cv.change_beta(days=dayptest1, changes=interv_eff),
#            cv.test_prob(symp_prob=0.5, asymp_prob=0.1, symp_quar_prob=1, asymp_quar_prob=0.1, loss_prob=0, test_delay=3,start_day=dayptest1),
#            cv.contact_tracing(trace_probs={'a': 0.8},trace_time={'a': 1},start_day=dayptest1,end_day=None)]
#        }
#    },
    'hightesttrace': { #isolate positive tests
        'name':'PPE, 90/50 test and ROM',
        'pars': {
            'quar_eff': {'a': 0.1},
            'quar_period': 14,
            'interventions': [cv.change_beta(days=dayptest1, changes=interv_eff),
            cv.test_prob(symp_prob=0.9, asymp_prob=0.5, symp_quar_prob=1, asymp_quar_prob=0.5, loss_prob=0, test_delay=3,start_day=dayptest1),
            cv.contact_tracing(trace_probs={'a': 0.8},trace_time={'a': 1},start_day=dayptest1,end_day=None)]
        }
    },
#              },
#            'tracing' : { # contact tracing
#              'name':'Trace',
#             'pars': {
#                  'quar_eff': 0.1,
#                  'quar_period': 14,
#                  'interventions': cv.contact_tracing(trace_probs=0.8,trace_time=1,start_day=0,end_day=None)
#                   }
#    },
}

if __name__ == "__main__": # Required for parallel processing on Windows

    sc.tic()

    # If we're rerunning...
    if do_run:
        scens = cv.Scenarios(basepars=basepars, metapars=metapars, scenarios=scenarios)
        scens.run(verbose=verbose)
        if do_save:
            scens.save(filename=obj_path)

    # Don't run
    else:
        scens = cv.Scenarios.load(obj_path)

    if do_plot:
        fig1 = scens.plot(do_show=do_show)

    sc.toc()
