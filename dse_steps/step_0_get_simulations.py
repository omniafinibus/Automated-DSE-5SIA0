# ======= # 
# Imports # 
# ======= # 
import os 
import subprocess
from copy import deepcopy

# =========== # 
# Definitions # 
# =========== # 
FREQ_LBL        = "$FREQ$"
CORE_LBL        = "$CORE$"

L1D_SIZE_LBL    = "$L1D_SIZE$"
L1D_ASSOC_LBL   = "$L1D_ASSOC$"
L1D_TYPE_LBL    = "$L1D_TYPE$"

L1I_SIZE_LBL    = "$L1I_SIZE$"
L1I_ASSOC_LBL   = "$L1I_ASSOC$"
L1I_TYPE_LBL    = "$L1I_TYPE$"

L2_ENABLED_LBL  = "$L2_ENABLED$"
L2_PREFETCH_LBL = "$L2_PREFETCH$"
L2_SIZE_LBL     = "$L2_SIZE$"
L2_ASSOC_LBL    = "$L2_ASSOC$"
L2_TYPE_LBL     = "$L2_TYPE$"

A15_LBL         = "A15"
A7_LBL          = "A7"
LOW_OP_POW_MODE = "\"lop\""
STDBY_MODE      = "\"lstp\""
HIGH_PERF_MODE  = "\"hp\""

HOME_DIR = "/" + os.path.join("DEFINE_BASE_DIR")
ANALYSIS_DIR = os.path.join(HOME_DIR, "analysis")
RESULTS_DIR = os.path.join(ANALYSIS_DIR, "results")
CONFIG_NAME = "simulation_parameters.py"
CONFIG_FILE = os.path.join(HOME_DIR, "gem5", "configs", CONFIG_NAME)
STATS_DIR = os.path.join(HOME_DIR, "gem5", "m5out")
STATS_FILE = os.path.join(STATS_DIR, "stats.txt")
BENCHMARK_DIR = os.path.join(HOME_DIR, "benchmark")
L_COMPLETED_TESTS = os.listdir(RESULTS_DIR)
SUMMARY_DIR = os.path.join(RESULTS_DIR, "summary.csv")

# ============ # 
# Data Classes # 
# ============ # 
class Cache:
    def __init__(self, name, size, assoc, type):
        self.name = name
        self.size = size
        self.assoc = assoc
        self.type = type
    
    def get_size_multiplier(self):
        """Convert the size string into a human readable size stirng

        :return: human readable size string
        :rtype: str
        """        
        base = self.size[:self.size.find(" ")]
        
        totalSize = newIndex = 0
        while(self.size.find("*", newIndex + 1) != -1):
            newIndex = self.size.find("*", newIndex + 1)
            totalSize += 1
        
        if totalSize == 1:
            return str(base) + "kB"
        elif totalSize == 2:
            return str(base) + "MB"
        elif totalSize == 0:
            return str(base) + "B"
        
class Configuration:
    def __init__(self, freq, core, l1d, l1i, l2_enabled, l2_prefetch, l2):
        self.freq = freq
        self.core = core
        self.l1d = l1d
        self.l1i = l1i
        self.l2_enabled = l2_enabled
        self.l2_prefetch = l2_prefetch
        self.l2 = l2
        self.fileName = ""

# ========= # 
# Functions # 
# ========= # 
def get_config_text(config
                    ):
    """Create the contents of a config file based on a custom configuration

    :param config: Configuration to read the parameters from
    :type config: Configuration
    :return: Contents of the new config file
    :rtype: str
    """    
    confTemp = os.path.join(ANALYSIS_DIR, "config_template.txt")
    print("[INFO]\tOpening file: " + confTemp)
    temp = open(confTemp, "r").read()
    temp = temp.replace(FREQ_LBL,        config.freq)
    temp = temp.replace(CORE_LBL,        config.core)
    temp = temp.replace(L1D_SIZE_LBL,    config.l1d.size)
    temp = temp.replace(L1D_ASSOC_LBL,   config.l1d.assoc)
    temp = temp.replace(L1D_TYPE_LBL,    config.l1d.type)
    temp = temp.replace(L1I_SIZE_LBL,    config.l1i.size)
    temp = temp.replace(L1I_ASSOC_LBL,   config.l1i.assoc)
    temp = temp.replace(L1I_TYPE_LBL,    config.l1i.type)
    temp = temp.replace(L2_ENABLED_LBL,  config.l2_enabled)
    temp = temp.replace(L2_PREFETCH_LBL, config.l2_prefetch)
    temp = temp.replace(L2_SIZE_LBL,     config.l2.size)
    temp = temp.replace(L2_ASSOC_LBL,    config.l2.assoc)
    temp = temp.replace(L2_TYPE_LBL,     config.l2.type)
    return temp

def replace_config(config):
    """Change the content of the config file with a new configuration

    :param config: Configuration to use for the file contents
    :type config: Configuration
    """    
    with open(CONFIG_FILE, "w") as file:
        file.write(get_config_text(config))

def run_simulation():
    """Run the simulation of the currently saved config

    :return: Exit statis of the simulation command
    :rtype: int
    """    
    os.chdir(BENCHMARK_DIR)
    command = "make simulate"
    print("[INFO]\tRunning command:" + command)
    return subprocess.call(command, shell=True)

def get_config_name(config, focusCache=None):
    """Save the current stat results into a new file with a name based on the entered config

    :param config: Configuration to base the name on
    :type config: Configuration
    :param focusCache: Cache for which the parameters are being tested, defaults to None
    :type focusCache: Cache, optional

    :return: Name based on configuration parameters
    :rtype: str
    """
    config_name = "stats_" + config.core + "_"
    if focusCache:
        config_name += focusCache.name + "_" + focusCache.type.replace("\"", "") + "_" + focusCache.get_size_multiplier() + "_" + focusCache.assoc
    else:
        config_name += config.freq + "MHz"
        
    if config.l2_enabled == "True":
        config_name += "_l2"
        if config.l2_prefetch == "True":
            config_name += "_prefetch.txt"
        else:
            config_name += ".txt"
    else:
        config_name += "default.txt"
    
    return config_name

def save_stats(config):
    """Save the current stat results into a new file with a name based on the entered config

    :param config: Configuration to base the name on
    :type config: Configuration
    """
    command = "cp " + STATS_FILE + " " + os.path.join(RESULTS_DIR, config.fileName)
    print("[INFO]\tRunning command:" + command)
    subprocess.call("cp " + STATS_FILE + " " + os.path.join(RESULTS_DIR, config.fileName), shell=True)
    
# ========= # 
# Variables # 
# ========= # 
defaultConfigs = Configuration(
    freq        ="1500", 
    core        =A15_LBL, 
    l1d         =Cache("L1D", "32 * 1024", "2", HIGH_PERF_MODE), 
    l1i         =Cache("L1I", "32 * 1024", "2", HIGH_PERF_MODE), 
    l2_enabled  ="True", 
    l2_prefetch ="True", 
    l2          =Cache("L2", "2 * 1024 * 1024", "16", HIGH_PERF_MODE)
)
    
lLowCacheSizes     = [str(2**n) + " * 1024" for n in range(3, 10)]
print(lLowCacheSizes)
lHighCacheSizes    = lLowCacheSizes + [str(2**n) + " * 1024 * 1024" for n in range(0, 10)]
print(lHighCacheSizes)
lCacheAssociative  = [str(int(2**n)) for n in range(0, 6)]
print(lCacheAssociative)
lPerfTypes         = [LOW_OP_POW_MODE, HIGH_PERF_MODE]#, STDBY_MODE]
lFrequencies       = [str(freq) for freq in range(500, 2100, 100)]
ltL2States         = [("True", "True"), ("True", "False"), ("False", "False")]

# =========== # 
# Get results # 
# =========== # 
lConfigs = list()
for core in [A15_LBL, A7_LBL]:
    # Test different frequencies
    for freq in lFrequencies:
        lConfigs.append(deepcopy(defaultConfigs))
        lConfigs[-1].freq = freq
        lConfigs[-1].core = core
        lConfigs[-1].fileName = get_config_name(lConfigs[-1])
    
    if core == A7_LBL:
        defaultConfigs.freq = "1200"
    
    # Focus on the effects of L2 being enabled / disabled
    for l2_state, prefetch_state in ltL2States:
        # Focus on the effects of L1I
        # Effects of perf type
        for perf in lPerfTypes:
            # Effects of cache size
            for size in lLowCacheSizes:
                lConfigs.append(deepcopy(defaultConfigs))
                lConfigs[-1].core = core
                lConfigs[-1].l1i.size = size
                lConfigs[-1].l1i.type = perf
                lConfigs[-1].l2_enabled = l2_state
                lConfigs[-1].l2_prefetch = prefetch_state
                lConfigs[-1].fileName = get_config_name(lConfigs[-1], lConfigs[-1].l1i)
            
            # Effects of Associative level
            for assoc in lCacheAssociative:
                lConfigs.append(deepcopy(defaultConfigs))
                lConfigs[-1].core = core
                lConfigs[-1].l1i.assoc = assoc
                lConfigs[-1].l1i.type = perf
                lConfigs[-1].l2_enabled = l2_state
                lConfigs[-1].l2_prefetch = prefetch_state
                lConfigs[-1].fileName = get_config_name(lConfigs[-1], lConfigs[-1].l1i)
        
        # Focus on the effects of L1D
        # Effects of perf type
        for perf in lPerfTypes:
            # Effects of cache size
            for size in lLowCacheSizes:
                lConfigs.append(deepcopy(defaultConfigs))
                lConfigs[-1].core = core
                lConfigs[-1].l1d.size = size
                lConfigs[-1].l1d.type = perf
                lConfigs[-1].l2_enabled = l2_state
                lConfigs[-1].l2_prefetch = prefetch_state
                lConfigs[-1].fileName = get_config_name(lConfigs[-1], lConfigs[-1].l1d)
            
            # Effects of Associative level
            for assoc in lCacheAssociative:
                lConfigs.append(deepcopy(defaultConfigs))
                lConfigs[-1].core = core
                lConfigs[-1].l1d.assoc = assoc
                lConfigs[-1].l1d.type = perf
                lConfigs[-1].l2_enabled = l2_state
                lConfigs[-1].l2_prefetch = prefetch_state
                lConfigs[-1].fileName = get_config_name(lConfigs[-1], lConfigs[-1].l1d)
    
    # Focus on the effects of L2
    # With L2 prefetch enabled / disabled
    for prefetch_state in ["True", "False"]:
        for perf in lPerfTypes:
            # Effects of cache size
            for size in lLowCacheSizes:
                lConfigs.append(deepcopy(defaultConfigs))
                lConfigs[-1].core = core
                lConfigs[-1].l2.size = size
                lConfigs[-1].l2.type = perf
                lConfigs[-1].l2_prefetch = prefetch_state
                lConfigs[-1].fileName = get_config_name(lConfigs[-1], lConfigs[-1].l2)
            
            # Effects of Associative level
            for assoc in lCacheAssociative:
                lConfigs.append(deepcopy(defaultConfigs))
                lConfigs[-1].core = core
                lConfigs[-1].l2.assoc = assoc
                lConfigs[-1].l2.type = perf
                lConfigs[-1].l2_prefetch = prefetch_state
                lConfigs[-1].fileName = get_config_name(lConfigs[-1], lConfigs[-1].l2)
    
for currentIndex, config in enumerate(lConfigs):
    if config.fileName in L_COMPLETED_TESTS:
        print("[INFO]\t[" + str(currentIndex + 1) + "\\" + str(len(lConfigs)) + "] Test already completered: " + config.fileName)
    else:    
        print("[INFO]\t[" + str(currentIndex + 1) + "\\" + str(len(lConfigs)) + "] " + config.fileName)
        replace_config(config)
        run_simulation()
        save_stats(config)