"""
Date: 2023 03 15

This plots the MSD vs tau for the averaged MCP1 and MCP6 data at both 298 and 310 K.

This also estimates the diffusion coefficient using bootstrapping methods.
"""
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import (inset_axes, InsetPosition,
                                                  mark_inset)
# for some reason, the mpl_toolkits.axes_grid1 requires the "grid1" on import INSTEAD 
# of "axes_grid." like what I've used previously and I think it's because of an update to 
# matplotlib that caused this.
# Current version I'm working with: 3.7.1
import numpy as np
import scipy.optimize as so

def bootstrap(Original_Data, Function, Nsample, Nbootstrap):
    """
    I will implement the bootstrap for this analysis as follows:
        1. Randomly pick a number from [1,2,3]
            This corresponds to picking data from either the 1st, 2nd, or 3rd replicate
        2. Randomly pick a number from [51:502]
            This corresponds to picking a data point from within the 5%-50% of the MSD
            data.
        3. Collect that point into a new array.
        4. Repeat 1-3 until I've reached the sample size.
        5. Perform linear regression on the new sample data
        6. Save the slope and intercept from this regression into a saving array
        7. Repeat 1-6 for however many times you want to do the bootstrap
        8. Calculate summary statistics on the collection of slopes and intercepts I've produced
    """
    
    slope_collection = []
    intercept_collection = []
    new_sample = np.zeros(Nsample)      # this holds the bootstrapped samples
    new_sampleTau = np.zeros(Nsample)   # this holds the corresponding Tau for each of the
                                        # bootstrapped samples so I can do the regression
    n = 1
    while n <= Nbootstrap:
        for I in range(Nsample):
            rand_int = np.random.randint(1, high=4)
            rand_data = np.random.randint(51, high=502)
            
            new_sample[I] = Original_Data[rand_data][rand_int]
            new_sampleTau[I] = Original_Data[rand_data][0]
        
        new_params, new_cov = so.curve_fit(Function, 
                xdata=new_sampleTau, 
                ydata=new_sample)
        slope_collection.append(new_params[0])
        intercept_collection.append(new_params[1])
                
        n += 1
    
    # now do the summary statistics for the collection of items
    average_slope = np.average(slope_collection)
    std_slope = np.std(slope_collection)
    average_incpt = np.average(intercept_collection)
    std_incpt = np.std(intercept_collection)

    return average_slope, std_slope, average_incpt, std_incpt


# Load up all the files and do some averaging
mcp1_298 = np.genfromtxt("mcp1_298_triplicateMSD.csv", delimiter=",")
mcp1_310 = np.genfromtxt("mcp1_310_triplicateMSD.csv", delimiter=",")
mcp6_298 = np.genfromtxt("mcp6_298_triplicateMSD.csv", delimiter=",")
mcp6_310 = np.genfromtxt("mcp6_310_triplicateMSD.csv", delimiter=",")


tau = mcp1_298[:,0]; tau[0] = 0.0
TAU = tau / 1000000

MCP1_298 = np.average(mcp1_298[:,1:4], axis=1); stdMCP1_298 = np.std(mcp1_298[:,1:4], axis=1)
MCP1_310 = np.average(mcp1_310[:,1:4], axis=1); stdMCP1_310 = np.std(mcp1_310[:,1:4], axis=1)

MCP6_298 = np.average(mcp6_298[:,1:4], axis=1); stdMCP6_298 = np.std(mcp6_298[:,1:4], axis=1)
MCP6_310 = np.average(mcp6_310[:,1:4], axis=1); stdMCP6_310 = np.std(mcp6_310[:,1:4], axis=1)




# Now it's time for the bootstrap itself!
linear = lambda x, m, b: x*m + b         # this is the linear function to fit to!
slope_mcp1_298, std_slope_mcp1_298, incpt_mcp1_298, std_incpt_mcp1_298 = bootstrap(mcp1_298, linear, 450, 5000)
slope_mcp1_310, std_slope_mcp1_310, incpt_mcp1_310, std_incpt_mcp1_310 = bootstrap(mcp1_310, linear, 450, 5000)
slope_mcp6_298, std_slope_mcp6_298, incpt_mcp6_298, std_incpt_mcp6_298 = bootstrap(mcp6_298, linear, 450, 5000)
slope_mcp6_310, std_slope_mcp6_310, incpt_mcp6_310, std_incpt_mcp6_310 = bootstrap(mcp6_310, linear, 450, 5000)

# Calculate diffusion coefficients!
# this converts the units to cm^2 / s
D_mcp1_298 = (slope_mcp1_298 / 6) * (1E12) * (1 / (1E7*1E7))
std_D_mcp1_298 = (std_slope_mcp1_298 / 6) * (1E12) * (1 / (1E7*1E7))

D_mcp1_310 = (slope_mcp1_310 / 6) * (1E12) * (1 / (1E7*1E7))
std_D_mcp1_310 = (std_slope_mcp1_310 / 6) * (1E12) * (1 / (1E7*1E7))

D_mcp6_298 = (slope_mcp6_298 / 6) * (1E12) * (1 / (1E7*1E7))
std_D_mcp6_298 = (std_slope_mcp6_298 / 6) * (1E12) * (1 / (1E7*1E7))

D_mcp6_310 = (slope_mcp6_310 / 6) * (1E12) * (1 / (1E7*1E7))
std_D_mcp6_310 = (std_slope_mcp6_310 / 6) * (1E12) * (1 / (1E7*1E7))

print("Summary of bootstrap analysis and summary statistics")

print()
print(f"Results for MCP-1 at 298 K")
print(f"Slope: {slope_mcp1_298}")
print(f"Intercept: {incpt_mcp1_298}")
print(f"Diffusion coefficient: {D_mcp1_298}")
print(f"Standard deviation: {std_D_mcp1_298}")
print()
print(f"Results for MCP-1 at 310 K")
print(f"Slope: {slope_mcp1_310}")
print(f"Intercept: {incpt_mcp1_310}")
print(f"Diffusion coefficient: {D_mcp1_310}")
print(f"Standard deviation: {std_D_mcp1_310}")
print()
print(f"Results for MCP-6 at 298 K")
print(f"Slope: {slope_mcp6_298}")
print(f"Intercept: {incpt_mcp6_298}")
print(f"Diffusion coefficient: {D_mcp6_298}")
print(f"Standard deviation: {std_D_mcp6_298}")
print()
print(f"Results for MCP-6 at 310 K")
print(f"Slope: {slope_mcp6_310}")
print(f"Intercept: {incpt_mcp6_310}")
print(f"Diffusion coefficient: {D_mcp6_310}")
print(f"Standard deviation: {std_D_mcp6_310}")





fig, ax1 = plt.subplots(figsize=(10,6))

plt.rcParams['font.size'] = 16
    
ax1.plot(TAU, MCP1_298, linestyle="-", color="cornflowerblue", label="T=298K, 3-heptad protein",
    linewidth=2)
ax1.plot(TAU[51:502], linear(tau[51:502], slope_mcp1_298, incpt_mcp1_298),
    linestyle="--", color="black")
ax1.fill_between(np.array(TAU), MCP1_298-stdMCP1_298, MCP1_298+stdMCP1_298, linewidth=0,
    color="cornflowerblue", alpha=0.45)

ax1.plot(TAU, MCP1_310, linestyle="-", color="palevioletred", label="T=310K, 3-heptad protein",
    linewidth=2)
ax1.plot(TAU[51:502], linear(tau[51:502], slope_mcp1_310, incpt_mcp1_310),
    linestyle="--", color="black")
ax1.fill_between(np.array(TAU), MCP1_310-stdMCP1_310, MCP1_310+stdMCP1_310, linewidth=0,
    color="palevioletred", alpha=0.45)
    
ax1.plot(TAU, MCP6_298, linestyle="-", color="deepskyblue", label="T=298K, 4-heptad protein",
    linewidth=2)
ax1.fill_between(np.array(TAU), MCP6_298-stdMCP6_298, MCP6_298+stdMCP6_298, linewidth=0,
    color="deepskyblue", alpha=0.45)

ax1.plot(TAU, MCP6_310, linestyle="-", color="plum", label="T=310K, 4-heptad protein",
    linewidth=2)
ax1.fill_between(np.array(TAU), MCP6_310-stdMCP6_310, MCP6_310+stdMCP6_310, linewidth=0,
    color="plum", alpha=0.45)

ax1.set_xticks(np.arange(0, 11, 1))
ax1.set_ylabel(f"MSD (nm$^{2}$)", fontsize=16)
ax1.set_xlabel(r"$\tau$ (us)", fontsize=16)
ax1.tick_params(axis='both', which='major', labelsize=14)
ax1.grid(linestyle=":", color="black", alpha=0.45)
    
    
# adding an inset to show the 4-heptad proteins better
ax2 = plt.axes([0,0,1,1])
# Manually set the position and relative size of the inset axes within ax1
# numbers are [left, bottom, width, height]
ip = InsetPosition(ax1, [0.1,0.58,0.4,0.4])
ax2.set_axes_locator(ip)
# Mark the region corresponding to the inset axes on ax1 and draw lines
# in grey linking the two axes.
# mark_inset(ax1, ax2, loc1=2, loc2=4, fc="none", ec='0.5')

ax2.plot(TAU, MCP6_298, linestyle="-", color="deepskyblue", label="T=298K, 4-heptad protein",
    linewidth=2)
ax2.plot(TAU[51:502], linear(tau[51:502], slope_mcp6_298, incpt_mcp6_298),
    linestyle="--", color="black")
ax2.fill_between(np.array(TAU), MCP6_298-stdMCP6_298, MCP6_298+stdMCP6_298, linewidth=0,
    color="deepskyblue", alpha=0.45)

ax2.plot(TAU, MCP6_310, linestyle="-", color="plum", label="T=310K, 4-heptad protein",
    linewidth=2)
ax2.plot(TAU[51:502], linear(tau[51:502], slope_mcp6_310, incpt_mcp6_310),
    linestyle="--", color="black")
ax2.fill_between(np.array(TAU), MCP6_310-stdMCP6_310, MCP6_310+stdMCP6_310, linewidth=0,
    color="plum", alpha=0.45)

ax2.set_xticks(np.arange(0, 11, 2))
ax2.set_ylabel(f"MSD (nm$^{2}$)", fontsize=12)
#ax2.set_ylim(0, 23)
ax2.set_xlabel(r"$\tau$ (us)", fontsize=12)
ax2.tick_params(axis='both', which='major', labelsize=10)
ax2.grid(linestyle=":", color="black", alpha=0.45)


# plt.legend()
leg = ax1.legend(fontsize='x-large', bbox_to_anchor=(1.05, 1.10), borderaxespad=0,
    edgecolor='black')
leg.get_frame().set_alpha(1)
# plt.tight_layout()
plt.savefig("MSD_bootstrap_analysis_plot.png", dpi=600)