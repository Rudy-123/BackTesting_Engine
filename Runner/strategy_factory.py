from Strategies.ma_crossover import MACrossoverStrategy
from itertools import product #Product give each possible combination of {short_window,long_window}

def generate_strategies(config):#input is the config dict and the output is the strategy parameter combinations
    strat_config=config["strategies"]["ma_crossover"]
    shorts=strat_config["short_window"]
    longs=strat_config["long_window"]
    strategies=[] #here all the valid strategy combos honge

    #Combination Generation
    for s,l in product(shorts,longs):
        if s<l: #else we would break the rule for the ma_crossover strategy
            strategies.append((s,l))
    return strategies

#so the all pairs of swindow and lwindows are generated 