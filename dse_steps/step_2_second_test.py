# ======= # 
# Imports # 
# ======= # 
import os 
from step_0_get_simulations import *
from step_1_process_results import Results, Power, CacheResults, extract_data
     
# ========= # 
# Functions # 
# ========= #
    
def save_stats(config, fileDir):
    """Save the current stat results into a result object

    :param config: Configuration which is used in the test
    :type config: Configuration
    :param fileDir: Directory of file to parse
    :type fileDir: str
    :return: converted data from the results file
    :rtype: Results
    """
    result = Results(
        exTime = 0.0,
        totalEnergy= 0.0,
        iCache=CacheResults(missRate=0.0, hits=0.0, misses=0.0),
        dCache=CacheResults(missRate=0.0, hits=0.0, misses=0.0),
        l2=CacheResults(missRate=0.0, hits=0.0, misses=0.0),
        config=config,
        power=Power()
    )
    
    with open(fileDir, "r") as file:
        for line in file.readlines():
            if line.find("sim_seconds") != -1:
                result.exTime += extract_data(line)
            elif line.find("system.mem_ctrls_0.totalEnergy") != -1:
                result.totalEnergy += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.icache.overall_hits::total") != -1:
                result.iCache.hits += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.icache.overall_misses::total") != -1:
                result.iCache.misses += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.icache.overall_miss_rate::total") != -1:
                result.iCache.missRate += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.dcache.overall_hits::total") != -1:
                result.dCache.hits += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.dcache.overall_misses::total") != -1:
                result.dCache.misses += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.dcache.overall_miss_rate::total") != -1:
                result.dCache.missRate += extract_data(line)
            elif line.find("system.cpu_cluster.l2.overall_hits::total") != -1:
                result.l2.hits += extract_data(line)
            elif line.find("system.cpu_cluster.l2.overall_misses::total") != -1:
                result.l2.misses += extract_data(line)
            elif line.find("system.cpu_cluster.l2.overall_miss_rate::total") != -1:
                result.l2.missRate += extract_data(line)
            elif line.find("system.mem_ctrls_0.refreshEnergy") != -1:
                result.power.refreshEnergy += extract_data(line)
            elif line.find("system.mem_ctrls_0.selfRefreshEnergy") != -1:
                result.power.selfRefreshEnergy += extract_data(line)
            elif line.find("system.mem_ctrls_0.actEnergy") != -1:
                result.power.actEnergy += extract_data(line)
            elif line.find("system.mem_ctrls_0.actBackEnergy") != -1:
                result.power.actBackEnergy += extract_data(line)
            elif line.find("system.mem_ctrls_0.actPowerDownEnergy") != -1:
                result.power.actPowerDownEnergy += extract_data(line)
            elif line.find("system.mem_ctrls_0.preEnergy") != -1:
                result.power.preEnergy += extract_data(line)
            elif line.find("system.mem_ctrls_0.preBackEnergy") != -1:
                result.power.preBackEnergy += extract_data(line)
            elif line.find("system.mem_ctrls_0.prePowerDownEnergy") != -1:
                result.power.prePowerDownEnergy += extract_data(line)
            elif line.find("system.mem_ctrls_0.readEnergy") != -1:
                result.power.readEnergy += extract_data(line)
            elif line.find("system.mem_ctrls_0.writeEnergy") != -1:
                result.power.writeEnergy += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.dcache.power_model.static_power")  != -1:
                result.power.dCacheStaticPower += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.dcache.power_model.dynamic_power")  != -1:
                result.power.dCacheDynamicPower += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.dtb_walker_cache.power_model.static_power")  != -1:
                result.power.dWalkerCacheStaticPower += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.dtb_walker_cache.power_model.dynamic_power")  != -1:
                result.power.dWalkerCacheDynamicPower += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.icache.power_model.static_power")  != -1:
                result.power.iCacheStaticPower += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.icache.power_model.dynamic_power")  != -1:
                result.power.iCacheDynamicPower += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.itb_walker_cache.power_model.static_power")  != -1:
                result.power.iWalkerCacheStaticPower += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.itb_walker_cache.power_model.dynamic_power")  != -1:
                result.power.iWalkerCacheDynamicPower += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.power_model.static_power" ) != -1:
                result.power.cpuStaticPower += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.power_model.dynamic_power" ) != -1:
                result.power.cpuDynamicPower += extract_data(line)
            elif line.find("system.cpu_cluster.l2.power_model.static_power" ) != -1:
                result.power.l2StaticPower += extract_data(line)
            elif line.find("system.cpu_cluster.l2.power_model.dynamic_power" ) != -1:
                result.power.l2DynamicPower += extract_data(line)
    
    return result

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
lResults = list()
for currentIndex, config in enumerate(lConfigs):
    if config.fileName in L_COMPLETED_TESTS:
        print("[INFO]\t[" + str(currentIndex + 1) + "\\" + str(len(lConfigs)) + "] Test already completered: " + config.fileName)
    else:    
        print("[INFO]\t[" + str(currentIndex + 1) + "\\" + str(len(lConfigs)) + "] " + config.fileName)
        replace_config(config)
        run_simulation()
        
        lResults.append(save_stats(config, STATS_FILE))

if os.path.isfile(SUMMARY_DIR):
    os.remove(SUMMARY_DIR)

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