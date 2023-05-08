# Soil water balance simulator


The project  uses daily rainfall data from 1st June to 12th November(165 days) to simulate the water content in the soil layers at an intermediary time point with the given soil and crop characteristics. Soil layer at a point is a one dimensional entity, spanning surface on the ground till a certain depth.  All quantities are therefore expressed in mm/meters.  Soil water balance is the distribution of rainfall (mm) into runoff, soil moisture, crop uptake and groundwater recharge.

![Visualization for soil water balance](/images/visualization.png "Visualization")

Conditions used for the simulation:

On any day, the following invariant must hold:
	rain(n) = sm(n) - sm(n-1) + runoff(n) + excess(n) + uptake(n) + gw(n)

On the last day of the simulation, the following must be true:
	∑rain(n) = sm(n) + ∑runoff(n) + ∑excess(n) + ∑uptake(n) + ∑gw(n)


## Requirements

Language used : python3.10

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pandas and matplotlib.

```bash
pip install pandas
pip install matplotlib
```

## Usage

Open terminal and run the following lines
```bash
git clone https://github.com/pranjalanimesh/soil-water-simulation
cd soil-water-simulation
```

```python
python3 -u main.py
```

## Results
![Deep - Shallow comparison](/images/plot.png "Simulation")


[Report Link](https://docs.google.com/document/d/1UM8dhPNutkYMMUpYnLMKuBbkwl-fSnNlT2vLhlq-XQ0/edit?usp=sharing)