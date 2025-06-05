# ======= # 
# Imports # 
# ======= # 
import os 
from step_0_get_simulations import *
from step_1_process_results import extract_data
        
# ========= # 
# Functions # 
# ========= # 

def combine_results(resultsOne, resultsTwo):
    resultsOne.exTime += resultsTwo.exTime
    resultsOne.totalEnergy += resultsTwo.totalEnergy
    resultsOne.iCache.hits += resultsTwo.iCache.hits
    resultsOne.iCache.misses += resultsTwo.iCache.misses
    resultsOne.iCache.missRate += resultsTwo.iCache.missRate
    resultsOne.dCache.hits += resultsTwo.dCache.hits
    resultsOne.dCache.misses += resultsTwo.dCache.misses
    resultsOne.dCache.missRate += resultsTwo.dCache.missRate
    resultsOne.l2.hits += resultsTwo.l2.hits
    resultsOne.l2.misses += resultsTwo.l2.misses
    resultsOne.l2.missRate += resultsTwo.l2.missRate
    resultsOne.power.refreshEnergy += resultsTwo.power.refreshEnergy
    resultsOne.power.selfRefreshEnergy += resultsTwo.power.selfRefreshEnergy
    resultsOne.power.actEnergy += resultsTwo.power.actEnergy
    resultsOne.power.actBackEnergy += resultsTwo.power.actBackEnergy
    resultsOne.power.actPowerDownEnergy += resultsTwo.power.actPowerDownEnergy
    resultsOne.power.preEnergy += resultsTwo.power.preEnergy
    resultsOne.power.preBackEnergy += resultsTwo.power.preBackEnergy
    resultsOne.power.prePowerDownEnergy += resultsTwo.power.prePowerDownEnergy
    resultsOne.power.readEnergy += resultsTwo.power.readEnergy
    resultsOne.power.writeEnergy += resultsTwo.power.writeEnergy
    resultsOne.power.dCacheStaticPower += resultsTwo.power.dCacheStaticPower
    resultsOne.power.dCacheDynamicPower += resultsTwo.power.dCacheDynamicPower
    resultsOne.power.dWalkerCacheStaticPower += resultsTwo.power.dWalkerCacheStaticPower
    resultsOne.power.dWalkerCacheDynamicPower += resultsTwo.power.dWalkerCacheDynamicPower
    resultsOne.power.iCacheStaticPower += resultsTwo.power.iCacheStaticPower
    resultsOne.power.iCacheDynamicPower += resultsTwo.power.iCacheDynamicPower
    resultsOne.power.iWalkerCacheStaticPower += resultsTwo.power.iWalkerCacheStaticPower
    resultsOne.power.iWalkerCacheDynamicPower += resultsTwo.power.iWalkerCacheDynamicPower
    resultsOne.power.cpuStaticPower += resultsTwo.power.cpuStaticPower
    resultsOne.power.cpuDynamicPower += resultsTwo.power.cpuDynamicPower
    resultsOne.power.l2StaticPower += resultsTwo.power.l2StaticPower
    resultsOne.power.l2DynamicPower += resultsTwo.power.l2DynamicPower
    return resultsOne

# =========== # 
# Get results # 
# =========== # 
lConfigs = [
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "16", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "8", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "32", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "8", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "64", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "8", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "16", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "8",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "8", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "32", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "8",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "8", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "64", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "8",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "8", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "16", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "16", HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "8", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "32", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "16", HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "8", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "64", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "16", HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "8", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "16", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "16", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "32", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "16", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "64", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "16", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "16", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "8",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "16", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "32", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "8",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "16", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "64", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "8",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "16", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "16", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "16", HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "16", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "32", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "16", HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "16", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "64", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "16", HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "16", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "16", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "32", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "64", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "16", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "8",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "32", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "8",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "16", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "8",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "32", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "16", HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "64", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "16", HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 1
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "16", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "16", HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 1
    
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "1", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "8", HIGH_PERF_MODE)), # 2
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "8", HIGH_PERF_MODE)), # 2
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "4", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "8", HIGH_PERF_MODE)), # 2
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "8", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "8", HIGH_PERF_MODE)), # 2
    
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "2", HIGH_PERF_MODE)), # 3
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "4", HIGH_PERF_MODE)), # 3
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "8", HIGH_PERF_MODE)), # 3
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "16", HIGH_PERF_MODE)), # 3
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "2 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 3
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "2", HIGH_PERF_MODE)), # 3
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "4", HIGH_PERF_MODE)), # 3
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "8", HIGH_PERF_MODE)), # 3
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "16", HIGH_PERF_MODE)), # 3
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 3
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "8 * 1024 * 1024", "2", HIGH_PERF_MODE)), # 3
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "8 * 1024 * 1024", "4", HIGH_PERF_MODE)), # 3
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "8 * 1024 * 1024", "8", HIGH_PERF_MODE)), # 3
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "8 * 1024 * 1024", "16", HIGH_PERF_MODE)), # 3
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "8 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 3
    
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "16 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "32 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "64 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4", HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "256 * 1024", "4", HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "256 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "16 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "256 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "32 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "256 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "64 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "256 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4", HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "256 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "256 * 1024", "4", HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "16 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "32 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "64 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4", HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "256 * 1024", "4", HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "16 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "2", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "32 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "2", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "64 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "2", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4", HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "2", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "256 * 1024", "4", HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "2", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "256 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "16 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "2", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "256 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "32 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "2", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "256 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "64 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "2", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "256 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4", HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "2", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "256 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "256 * 1024", "4", HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "2", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "16 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "2", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "32 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "2", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "64 * 1024", "4",  HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "2", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "128 * 1024", "4", HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "2", HIGH_PERF_MODE)), # 4
    Configuration("1500", "A15", Cache("L1D", "512 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "256 * 1024", "4", HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "2", HIGH_PERF_MODE)), # 4
        
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "32 * 1024", "4", HIGH_PERF_MODE), "True", "True", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 5
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "32 * 1024", "4", HIGH_PERF_MODE), "True", "True", Cache("L2", "4 * 1024 * 1024", "32", LOW_OP_POW_MODE)), # 5
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "32 * 1024", "4", LOW_OP_POW_MODE), "True", "True", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 5
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "32 * 1024", "4", LOW_OP_POW_MODE), "True", "True", Cache("L2", "4 * 1024 * 1024", "32", LOW_OP_POW_MODE)), # 5
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", LOW_OP_POW_MODE), Cache("L1I", "32 * 1024", "4", HIGH_PERF_MODE), "True", "True", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 5
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", LOW_OP_POW_MODE), Cache("L1I", "32 * 1024", "4", HIGH_PERF_MODE), "True", "True", Cache("L2", "4 * 1024 * 1024", "32", LOW_OP_POW_MODE)), # 5
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", LOW_OP_POW_MODE), Cache("L1I", "32 * 1024", "4", HIGH_PERF_MODE), "True", "True", Cache("L2", "4 * 1024 * 1024", "32", LOW_OP_POW_MODE)), # 5
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", LOW_OP_POW_MODE), Cache("L1I", "32 * 1024", "4", LOW_OP_POW_MODE), "True", "True", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 5
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", LOW_OP_POW_MODE), Cache("L1I", "32 * 1024", "4", LOW_OP_POW_MODE), "True", "True", Cache("L2", "4 * 1024 * 1024", "32", LOW_OP_POW_MODE)), # 5
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "32 * 1024", "4", HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 5
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "32 * 1024", "4", HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", LOW_OP_POW_MODE)), # 5
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "32 * 1024", "4", LOW_OP_POW_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 5
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", HIGH_PERF_MODE), Cache("L1I", "32 * 1024", "4", LOW_OP_POW_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", LOW_OP_POW_MODE)), # 5
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", LOW_OP_POW_MODE), Cache("L1I", "32 * 1024", "4", HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 5
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", LOW_OP_POW_MODE), Cache("L1I", "32 * 1024", "4", HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", LOW_OP_POW_MODE)), # 5
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", LOW_OP_POW_MODE), Cache("L1I", "32 * 1024", "4", HIGH_PERF_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", LOW_OP_POW_MODE)), # 5
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", LOW_OP_POW_MODE), Cache("L1I", "32 * 1024", "4", LOW_OP_POW_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", HIGH_PERF_MODE)), # 5
    Configuration("1500", "A15", Cache("L1D", "128 * 1024", "2", LOW_OP_POW_MODE), Cache("L1I", "32 * 1024", "4", LOW_OP_POW_MODE), "True", "False", Cache("L2", "4 * 1024 * 1024", "32", LOW_OP_POW_MODE)), # 5
]

lStats = [os.path.join(STATS_DIR, "im" + str(i), "stats.txt") for i in range(2,15)]

lResults = list()

if os.path.isfile(SUMMARY_DIR):
    os.remove(SUMMARY_DIR)
    
for config in lConfigs:
    replace_config(config)
    run_simulation()
    
    result = save_stats(config, os.path.join(STATS_DIR, "im1", "stats.txt"))
    result.config = config
    for statFile in lStats:
        result = combine_results(result, save_stats(config, statFile))
    
    lResults.append(result)
        
with open(SUMMARY_DIR, 'w') as file:
    file.write("freq,core,L1D_size,L1D_assoc,L1D_type,L1I_size,L1I_assoc,L1I_type,l2_enabled,l2_prefetch,L2_size,L2_assoc,L2_type,benchmark,sim_seconds,total_energy,l1i_hits,l1i_misses,l1i_miss_rate,l1d_hits,l1d_misses,l1d_miss_rate,l2_hits,l2_misses,l2_miss_rate,refreshEnergy,selfRefreshEnergy,actEnergy,actBackEnergy,actPowerDownEnergy,preEnergy,preBackEnergy,prePowerDownEnergy,readEnergy,writeEnergy,dCacheStaticPower,dCacheDynamicPower,dWalkerCacheStaticPower,dWalkerCacheDynamicPower,iCacheStaticPower,iCacheDynamicPower,iWalkerCacheStaticPower,iWalkerCacheDynamicPower,cpuStaticPower,cpuDynamicPower,l2StaticPower,l2DynamicPower\n")
    for result in lResults:
        file.write(result.config.freq + ",")                         # freq
        file.write(result.config.core + ",")                         # core
        file.write(result.config.l1d.get_size_multiplier() + ",")    # L1D size
        file.write(result.config.l1d.assoc + ",")                    # L1D assoc
        file.write(result.config.l1d.type + ",")                     # L1D type
        file.write(result.config.l1i.get_size_multiplier() + ",")    # L1I size
        file.write(result.config.l1i.assoc + ",")                    # L1I assoc
        file.write(result.config.l1i.type + ",")                     # L1I type
        file.write(result.config.l2_enabled + ",")                   # l2_enabled
        file.write(result.config.l2_prefetch + ",")                  # l2_prefetch
        file.write(result.config.l2.get_size_multiplier() + ",")     # L2 size
        file.write(result.config.l2.assoc + ",")                     # L2 assoc
        file.write(result.config.l2.type + ",")                      # L2 type
        file.write(str(result.exTime * (result.totalEnergy * (10**(-12)))) + ",") # benchmark
        file.write(str(result.exTime) + ",")                         # sim_seconds
        file.write(str(result.totalEnergy) + ",")                    # total_energy
        file.write(str(result.iCache.hits) + ",")                    # l1i_hits
        file.write(str(result.iCache.misses) + ",")                  # l1i_misses
        file.write(str(result.iCache.missRate) + ",")                # l1i_miss_rate
        file.write(str(result.dCache.hits) + ",")                    # l1d_hits
        file.write(str(result.dCache.misses) + ",")                  # l1d_misses
        file.write(str(result.dCache.missRate) + ",")                # l1d_miss_rate
        file.write(str(result.l2.hits) + ",")                        # l2_hits
        file.write(str(result.l2.misses) + ",")                      # l2_misses
        file.write(str(result.l2.missRate) + ",")                    # l2_miss_rate
        file.write(str(result.power.refreshEnergy) + ",")            # refreshEnergy            
        file.write(str(result.power.selfRefreshEnergy) + ",")        # selfRefreshEnergy                
        file.write(str(result.power.actEnergy) + ",")                # actEnergy        
        file.write(str(result.power.actBackEnergy) + ",")            # actBackEnergy            
        file.write(str(result.power.actPowerDownEnergy) + ",")       # actPowerDownEnergy                
        file.write(str(result.power.preEnergy) + ",")                # preEnergy        
        file.write(str(result.power.preBackEnergy) + ",")            # preBackEnergy            
        file.write(str(result.power.prePowerDownEnergy) + ",")       # prePowerDownEnergy                
        file.write(str(result.power.readEnergy) + ",")               # readEnergy        
        file.write(str(result.power.writeEnergy) + ",")              # writeEnergy                                   
        file.write(str(result.power.dCacheStaticPower) + ",")        # dCacheStaticPower
        file.write(str(result.power.dCacheDynamicPower) + ",")       # dCacheDynamicPower
        file.write(str(result.power.dWalkerCacheStaticPower) + ",")  # dWalkerCacheStaticPower
        file.write(str(result.power.dWalkerCacheDynamicPower) + ",") # dWalkerCacheDynamicPower
        file.write(str(result.power.iCacheStaticPower) + ",")        # iCacheStaticPower
        file.write(str(result.power.iCacheDynamicPower) + ",")       # iCacheDynamicPower
        file.write(str(result.power.iWalkerCacheStaticPower) + ",")  # iWalkerCacheStaticPower
        file.write(str(result.power.iWalkerCacheDynamicPower) + ",") # iWalkerCacheDynamicPower
        file.write(str(result.power.cpuStaticPower) + ",")           # cpuStaticPower
        file.write(str(result.power.cpuDynamicPower) + ",")          # cpuDynamicPower
        file.write(str(result.power.l2StaticPower) + ",")            # l2StaticPower
        file.write(str(result.power.l2DynamicPower) + "\n")          # l2DynamicPower