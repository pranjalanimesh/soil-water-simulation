# Importing and configuring libraries 
import pandas as pd
pd.set_option('mode.chained_assignment', None)
import matplotlib.pyplot as plt

# Import rainfall data
df = pd.read_csv('daily_rainfall_jalgaon_chalisgaon_talegaon_2022.csv')
df.head()

# Initializing simulation template dataframe 
cols = ['Day', 'Rainfall','Runoff + excess','Crop water uptake','Soil moisture','Percolation of ground water']
sim_temp = pd.DataFrame(index = range(len(df)) , columns=cols)
sim_temp['Day'] = df['date']
sim_temp['Rainfall'] = df['rain_mm']

# Values given
deep_C = 100
deep_gamma = 0.2
shallow_C = 42
shallow_gamma = 0.4

# Initializing the first day values of the simulation with zeroes
sim_temp.iloc[0,[2,3,4,5]]=0

# Define runoff function 
def runoff(rainfall):   # Outputs the running off water
    if rainfall<25:
        return 0.2*rainfall
    elif rainfall<50:
        return 0.3*rainfall
    elif rainfall<75:
        return 0.4*rainfall
    elif rainfall<100:
        return 0.5*rainfall
    elif rainfall>= 100:
        return 0.7*rainfall

# Define simulation function
def simulate(gamma, c):
    sim = sim_temp.__deepcopy__()
    for i in range(1,len(df)):
        rainfall = sim['Rainfall'][i]
        water_content = rainfall + sim['Soil moisture'][i-1]

        run = runoff(rainfall)
        uptake = 0
        excess = 0
        gw = 0
        sm = 0
        water_content -= run

        if water_content>=4:
            uptake+=4
            water_content-=4
        else:
            uptake = water_content
            water_content=0

        if water_content/(1+gamma) > c:
            sm = c
            excess = water_content - c*(1+gamma)
        else:
            sm = water_content/(1+gamma)

        gw = gamma*sm

        sim['Soil moisture'][i] = sm
        sim['Runoff + excess'][i] = run + excess
        sim['Crop water uptake'][i] = uptake
        sim['Percolation of ground water'][i] = gw

    return sim


# Deep soil simulation
deep_soil_sim = simulate(deep_gamma,deep_C)

# Shallow soil simulation
shallow_soil_sim = simulate(shallow_gamma,shallow_C)

# Verifying the simulation
for i in range(1,len(df)):
    x = 0
    if 0.00001 <= -deep_soil_sim['Rainfall'][i] + deep_soil_sim['Soil moisture'][i] - deep_soil_sim['Soil moisture'][i-1] + deep_soil_sim['Runoff + excess'][i] + deep_soil_sim['Crop water uptake'][i] + deep_soil_sim['Percolation of ground water'][i]:
        x=1
print('Deep soil')
if x==0:
    print('All rows satisfies the first condition.')
    print()
else:
    print('Some Problem')


for i in range(1,len(df)):
    x = 0
    if 0.00001 <= -shallow_soil_sim['Rainfall'][i] + shallow_soil_sim['Soil moisture'][i] - shallow_soil_sim['Soil moisture'][i-1] + shallow_soil_sim['Runoff + excess'][i] + shallow_soil_sim['Crop water uptake'][i] + shallow_soil_sim['Percolation of ground water'][i]:
        x=1
print('Shallow soil')
if x==0:
    print('All rows satisfies the first condition.')
    print()
else:
    print('Some Problem')
print()
deep_sums= deep_soil_sim.sum()
shallow_sums= shallow_soil_sim.sum()

print('Validating second condition for the simulations\n')

print('For deep soil simulation')
print('Total rainfall:' , list(deep_sums)[1])
print('Sum of total runoff + excess, uptake and ground water:' ,round(list(deep_sums)[2]+list(deep_sums)[3]+list(deep_sums)[5] , 2))
print()
print('For shallow soil simulation')
print('Total rainfall:' , list(shallow_sums)[1])
print('Sum of total runoff + excess, uptake and ground water:' ,round(list(shallow_sums)[2]+list(shallow_sums)[3]+list(shallow_sums)[5],2))

print()
print('Deep soil crop total uptake:',list(deep_sums)[3])
print('Shallow soil crop total uptake:',list(shallow_sums)[3])
print()
print('Deep soil total runoff/excess:',list(deep_sums)[2])
print('Shallow soil total runoff/excess:',list(shallow_sums)[2])
print()
print('Deep soil total ground water percolation:',list(deep_sums)[5])
print('Shallow soil total ground water percolation:',list(shallow_sums)[5])

# Exporting simulation CSVs
deep_soil_sim.to_csv('./output/deep_soil_simulation.csv')
shallow_soil_sim.to_csv('./output/shallow_soil_simulation.csv')


# Ploting Rainfall, uptake and ground water levels in deep soil and shallow soil
fig, axes = plt.subplots(1, 2)
ax = axes[0]
ax.plot(deep_soil_sim.index,deep_soil_sim['Rainfall'],'r')
ax.plot(deep_soil_sim.index,deep_soil_sim.cumsum(axis=0)['Crop water uptake'],'g')
ax.plot(deep_soil_sim.index,deep_soil_sim.cumsum(axis=0)['Percolation of ground water'],'b')
ax.plot(deep_soil_sim.index,deep_soil_sim.cumsum(axis=0)['Runoff + excess'],'black')
ax.set_title('Deep soil')
ax.set_xlabel('Days')
ax.set_ylabel('Water(in mm)')
ax.legend(['Rainfall','Water Uptake(cumulative)','Ground water(cumulative)','Runoff/excess(cumulative)'])

ax = axes[1]
ax.plot(shallow_soil_sim.index,shallow_soil_sim['Rainfall'],'r')
ax.plot(shallow_soil_sim.index,shallow_soil_sim.cumsum(axis=0)['Crop water uptake'],'g')
ax.plot(shallow_soil_sim.index,shallow_soil_sim.cumsum(axis=0)['Percolation of ground water'],'b')
ax.plot(shallow_soil_sim.index,shallow_soil_sim.cumsum(axis=0)['Runoff + excess'],'black')
ax.set_title('Shallow soil')
ax.set_xlabel('Days')
ax.set_ylabel('Water(in mm)')
ax.legend(['Rainfall','Water Uptake(cumulative)','Ground water(cumulative)','Runoff/excess(cumulative)'])

fig.suptitle('Simulated plots')
fig.set_figwidth(10)
fig.tight_layout()
plt.show()