# ======= # 
# Imports # 
# ======= # 
import os 
from step_0_get_simulations import Cache, Configuration, A15_LBL, A7_LBL, LOW_OP_POW_MODE, STDBY_MODE, HIGH_PERF_MODE

# =========== # 
# Definitions # 
# =========== # 
HOME_DIR = "/" + os.path.join("DEFINE_BASE_DIR")
ANALYSIS_DIR = os.path.join(HOME_DIR,  "auto_tester_script")
RESULTS_DIR = os.path.join(ANALYSIS_DIR, "results")
SUMMARY_DIR = os.path.join(RESULTS_DIR, "summary_with_power.csv")

if os.path.isfile(SUMMARY_DIR):
    os.remove(SUMMARY_DIR)

L1D_FOCUS = "L1D"
L1I_FOCUS = "L1I"
L2_FOCUS = "L2"
FREQ_FOCUS = "FREQ"

# ============ # 
# Data Classes # 
# ============ #         
class CacheResults:
    def __init__(self, missRate, misses, hits):
        self.missRate = missRate
        self.misses = misses
        self.hits = hits

class Results:
    def __init__(self, exTime=0, totalEnergy=0, iCache=0, dCache=0, l2=0, focus=0, config=0, file=0, power=0):
        self.exTime = exTime
        self.totalEnergy = totalEnergy
        self.iCache = iCache
        self.dCache = dCache
        self.l2 = l2
        self.focus = focus
        self.file = file
        self.config = config
        self.power = power

class Power:
    def __init__(self):
        self.refreshEnergy = 0.0
        self.selfRefreshEnergy = 0.0
        self.actEnergy = 0.0
        self.actBackEnergy = 0.0
        self.actPowerDownEnergy = 0.0
        self.preEnergy = 0.0
        self.preBackEnergy = 0.0
        self.prePowerDownEnergy = 0.0
        self.readEnergy = 0.0
        self.writeEnergy = 0.0
        self.dCacheStaticPower = 0.0
        self.dCacheDynamicPower = 0.0
        self.dWalkerCacheStaticPower = 0.0
        self.dWalkerCacheDynamicPower = 0.0
        self.iCacheStaticPower = 0.0
        self.iCacheDynamicPower = 0.0
        self.iWalkerCacheStaticPower = 0.0
        self.iWalkerCacheDynamicPower = 0.0
        self.cpuStaticPower = 0.0
        self.cpuDynamicPower = 0.0
        self.l2StaticPower = 0.0
        self.l2DynamicPower = 0.0
        
# ========= # 
# Functions # 
# ========= # 
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def get_config(fileName):
    """Build a config object based on the file name

    :param fileName: Name of the stats file to be read
    :type fileName: str
    :return: Configuration based on the stats file
    :rtype: Configuration
    """    
    global defaultConfigs
    newConfig = Configuration(
        freq        ="1500", 
        core        =A15_LBL, 
        l1d         =Cache("L1D", "32kB", "2", HIGH_PERF_MODE), 
        l1i         =Cache("L1I", "32kB", "2", HIGH_PERF_MODE), 
        l2_enabled  ="True", 
        l2_prefetch ="True", 
        l2          =Cache("L2", "2MB", "16", HIGH_PERF_MODE)
    )
    fileName = fileName.replace("stats_", "")
    
    # Check which core was used
    if fileName.find(A15_LBL) != -1:
        newConfig.core = A15_LBL
        fileName = fileName.replace(A15_LBL + "_", "")
    else:
        newConfig.core = A7_LBL
        fileName = fileName.replace(A7_LBL + "_", "")
    
    # Check what was the focus of the test
    # L1D
    if fileName[:3] == "L1D":
        fileName = fileName.replace("L1D_", "")
        newCache, fileName = get_cache(fileName, "L1D")
        focus = L1D_FOCUS
        newConfig.l1d = newCache
    # L1I
    elif fileName[:3] == "L1I":
        fileName = fileName.replace("L1I_", "")
        newCache, fileName = get_cache(fileName, "L1I")
        focus = L1I_FOCUS
        newConfig.l1i = newCache
    # L2
    elif fileName[:2] == "L2":
        fileName = fileName.replace("L2_", "")
        newCache, fileName = get_cache(fileName, "L2")
        focus = L2_FOCUS
        newConfig.l2 = newCache
    # Frequency
    elif is_number(fileName[0]):
        index = fileName.find("MHz")
        newConfig.freq = fileName[:index]
        focus = FREQ_FOCUS
        fileName = fileName.replace(newConfig.freq + "_", "")
    
    if fileName[:2] == "l2":
        newConfig.l2_enabled = "True"
        fileName = fileName[3:]
        if fileName.find("prefetch"):
            newConfig.l2_prefetch = "True"
        else:
            newConfig.l2_prefetch = "False"
    else:
        newConfig.l2_enabled = "False"
        newConfig.l2_prefetch = "False"
    
    return newConfig, focus

def get_cache(fileName, name):
    # Get performance mode
    if fileName.find("hp") != -1:
        cacheType = HIGH_PERF_MODE
        fileName = fileName[3:]
    elif fileName.find("lop") != -1:
        cacheType = LOW_OP_POW_MODE
        fileName = fileName[4:]
        
    # Size
    index = fileName.find("kB")
    if index != -1:
        size = fileName[:index + 2]+"kB"
    else:
        index = fileName.find("MB")
        size = fileName[:index + 2]+"MB"
    fileName = fileName[index + 3:]

    # Association
    index = fileName.find("_")
    assoc = fileName[:index]
    fileName = fileName[index + 1:]

    return Cache(name, size, assoc, cacheType), fileName

def extract_data(line):
    """Extract data from a stats line

    :param line: Line to read data from
    :type line: str
    :return: Value read from the line
    :rtype: float
    """    
    
    og = line
    while(line.find("  ") != -1):
        line = line.replace("  ", " ")

    index1 = line.find(" ")
    line = line[index1+1:]
    index2 = line.find(" ")
    line = line[:index2]
    try:
        return float(line)
    except:
        print("couldn't convert: " + og + "  to float  ," + line)

# =========== # 
# Get results # 
# =========== # 
lStatsFiles = os.listdir(RESULTS_DIR)
lStatsFiles.remove("summary.csv")

lResults = list()
for index, statFile in enumerate(lStatsFiles):
    print("[INFO]\t[" + str(index + 1) + "\\" + str(len(lStatsFiles)) + "] Converting file " + statFile)
    fileDir = os.path.join(RESULTS_DIR, statFile)
    config, focus = get_config(statFile)
    lResults.append(Results(
        exTime = 0.0,
        totalEnergy= 0.0,
        iCache=CacheResults(missRate=0.0, hits=0.0, misses=0.0),
        dCache=CacheResults(missRate=0.0, hits=0.0, misses=0.0),
        l2=CacheResults(missRate=0.0, hits=0.0, misses=0.0),
        focus=focus,
        config=config,
        file=statFile,
        power=Power()
    ))
    
    with open(fileDir, "r") as file:
        for line in file.readlines():
            if line.find("sim_seconds") != -1:
                lResults[-1].exTime += extract_data(line)
            elif line.find("system.mem_ctrls_0.totalEnergy") != -1:
                lResults[-1].totalEnergy += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.icache.overall_hits::total") != -1:
                lResults[-1].iCache.hits += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.icache.overall_misses::total") != -1:
                lResults[-1].iCache.misses += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.icache.overall_miss_rate::total") != -1:
                lResults[-1].iCache.missRate += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.dcache.overall_hits::total") != -1:
                lResults[-1].dCache.hits += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.dcache.overall_misses::total") != -1:
                lResults[-1].dCache.misses += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.dcache.overall_miss_rate::total") != -1:
                lResults[-1].dCache.missRate += extract_data(line)
            elif line.find("system.cpu_cluster.l2.overall_hits::total") != -1:
                lResults[-1].l2.hits += extract_data(line)
            elif line.find("system.cpu_cluster.l2.overall_misses::total") != -1:
                lResults[-1].l2.misses += extract_data(line)
            elif line.find("system.cpu_cluster.l2.overall_miss_rate::total") != -1:
                lResults[-1].l2.missRate += extract_data(line)
            elif line.find("system.mem_ctrls_0.refreshEnergy") != -1:
                lResults[-1].power.refreshEnergy += extract_data(line)
            elif line.find("system.mem_ctrls_0.selfRefreshEnergy") != -1:
                lResults[-1].power.selfRefreshEnergy += extract_data(line)
            elif line.find("system.mem_ctrls_0.actEnergy") != -1:
                lResults[-1].power.actEnergy += extract_data(line)
            elif line.find("system.mem_ctrls_0.actBackEnergy") != -1:
                lResults[-1].power.actBackEnergy += extract_data(line)
            elif line.find("system.mem_ctrls_0.actPowerDownEnergy") != -1:
                lResults[-1].power.actPowerDownEnergy += extract_data(line)
            elif line.find("system.mem_ctrls_0.preEnergy") != -1:
                lResults[-1].power.preEnergy += extract_data(line)
            elif line.find("system.mem_ctrls_0.preBackEnergy") != -1:
                lResults[-1].power.preBackEnergy += extract_data(line)
            elif line.find("system.mem_ctrls_0.prePowerDownEnergy") != -1:
                lResults[-1].power.prePowerDownEnergy += extract_data(line)
            elif line.find("system.mem_ctrls_0.readEnergy") != -1:
                lResults[-1].power.readEnergy += extract_data(line)
            elif line.find("system.mem_ctrls_0.writeEnergy") != -1:
                lResults[-1].power.writeEnergy += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.dcache.power_model.static_power")  != -1:
                lResults[-1].power.dCacheStaticPower += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.dcache.power_model.dynamic_power")  != -1:
                lResults[-1].power.dCacheDynamicPower += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.dtb_walker_cache.power_model.static_power")  != -1:
                lResults[-1].power.dWalkerCacheStaticPower += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.dtb_walker_cache.power_model.dynamic_power")  != -1:
                lResults[-1].power.dWalkerCacheDynamicPower += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.icache.power_model.static_power")  != -1:
                lResults[-1].power.iCacheStaticPower += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.icache.power_model.dynamic_power")  != -1:
                lResults[-1].power.iCacheDynamicPower += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.itb_walker_cache.power_model.static_power")  != -1:
                lResults[-1].power.iWalkerCacheStaticPower += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.itb_walker_cache.power_model.dynamic_power")  != -1:
                lResults[-1].power.iWalkerCacheDynamicPower += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.power_model.static_power" ) != -1:
                lResults[-1].power.cpuStaticPower += extract_data(line)
            elif line.find("system.cpu_cluster.cpus.power_model.dynamic_power" ) != -1:
                lResults[-1].power.cpuDynamicPower += extract_data(line)
            elif line.find("system.cpu_cluster.l2.power_model.static_power" ) != -1:
                lResults[-1].power.l2StaticPower += extract_data(line)
            elif line.find("system.cpu_cluster.l2.power_model.dynamic_power" ) != -1:
                lResults[-1].power.l2DynamicPower += extract_data(line)
    
with open(SUMMARY_DIR, 'w') as file:
    file.write("freq,core,L1D_size,L1D_assoc,L1D_type,L1I_size,L1I_assoc,L1I_type,l2_enabled,l2_prefetch,L2_size,L2_assoc,L2_type,focus,benchmark,sim_seconds,total_energy,l1i_hits,l1i_misses,l1i_miss_rate,l1d_hits,l1d_misses,l1d_miss_rate,l2_hits,l2_misses,l2_miss_rate,refreshEnergy,selfRefreshEnergy,actEnergy,actBackEnergy,actPowerDownEnergy,preEnergy,preBackEnergy,prePowerDownEnergy,readEnergy,writeEnergy,dCacheStaticPower,dCacheDynamicPower,dWalkerCacheStaticPower,dWalkerCacheDynamicPower,iCacheStaticPower,iCacheDynamicPower,iWalkerCacheStaticPower,iWalkerCacheDynamicPower,cpuStaticPower,cpuDynamicPower,l2StaticPower,l2DynamicPower\n")
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
        file.write(result.focus + ",")                               # Focus
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