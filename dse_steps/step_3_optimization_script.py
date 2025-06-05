# ======= # 
# Imports # 
# ======= # 
import os 
import subprocess
from step_0_get_simulations import *
from step_2_second_test import save_stats

# ========= # 
# Functions # 
# ========= # 

def run_simulation():
    """Run the simulation of the currently saved config
    """    
    os.chdir(BENCHMARK_DIR)
    command = "make simulate"
    print("[INFO]\tRunning command:" + command)
    subprocess.call(command, shell=True)
    command = "(ristretto results/lincoln_out.bmp &)"
    print("[INFO]\tRunning command:" + command)
    subprocess.call(command, shell=True)
    


# =========== # 
# Get results # 
# =========== # 
run_simulation()

if os.path.isfile(SUMMARY_DIR):
    os.remove(SUMMARY_DIR)

result = save_stats(STATS_FILE)
with open(SUMMARY_DIR, 'w') as file:
    file.write("benchmark,sim_seconds,total_energy,l1i_hits,l1i_misses,l1i_miss_rate,l1d_hits,l1d_misses,l1d_miss_rate,l2_hits,l2_misses,l2_miss_rate,refreshEnergy,selfRefreshEnergy,actEnergy,actBackEnergy,actPowerDownEnergy,preEnergy,preBackEnergy,prePowerDownEnergy,readEnergy,writeEnergy,dCacheStaticPower,dCacheDynamicPower,dWalkerCacheStaticPower,dWalkerCacheDynamicPower,iCacheStaticPower,iCacheDynamicPower,iWalkerCacheStaticPower,iWalkerCacheDynamicPower,cpuStaticPower,cpuDynamicPower,l2StaticPower,l2DynamicPower\n")
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