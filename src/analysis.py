import pandas as pd
import numpy as np
import tkinter
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns


xlsb_file = '../data/2007-2024-PIT-Counts-by-CoC.xlsb'
all_fay_data = []

with pd.ExcelFile(xlsb_file, engine='pyxlsb') as xlsb:
    for sheet in xlsb.sheet_names:
        df = pd.read_excel(xlsb, sheet_name=sheet, engine='pyxlsb')
        
        if 'CoC Name' not in df.columns:
            continue

        fay_df = df[df['CoC Name'].astype(str).str.contains('Fayetteville/Cum', case=False, na=False)]
        
        if not fay_df.empty:
            # Insert 'Year' column at position 0
            fay_df.insert(0, 'Year', sheet)
            all_fay_data.append(fay_df)

# Combine all sheets into one DataFrame
fay_all_years = pd.concat(all_fay_data, ignore_index=True)
fay_all_years = fay_all_years.iloc[::-1].reset_index(drop=True)


# Ensure 'Year' is treated as a string or category for correct plotting order
fay_all_years['Year'] = fay_all_years['Year'].astype(str)
fay_all_years = fay_all_years.sort_values('Year')

# Set the overall style
sns.set_theme(style="whitegrid")

# Create subplots
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Fayetteville Homeless Trends by Category', fontsize=16, weight='bold')

# Plot 1: Overall Homeless
sns.lineplot(data=fay_all_years, x='Year', y='Overall Homeless', ax=axs[0, 0], marker='o')
axs[0, 0].set_title('Overall Homeless')
axs[0, 0].tick_params(axis='x', rotation=45)

# Plot 2: Under 18
sns.lineplot(data=fay_all_years, x='Year', y='Overall Homeless - Under 18', ax=axs[0, 1], marker='o')
axs[0, 1].set_title('Homeless Under 18')
axs[0, 1].tick_params(axis='x', rotation=45)

# Plot 3: Women
sns.lineplot(data=fay_all_years, x='Year', y='Overall Homeless - Woman', ax=axs[1, 0], marker='o')
axs[1, 0].set_title('Homeless Women')
axs[1, 0].tick_params(axis='x', rotation=45)

# Plot 4: Men
sns.lineplot(data=fay_all_years, x='Year', y='Overall Homeless - Man', ax=axs[1, 1], marker='o')
axs[1, 1].set_title('Homeless Men')
axs[1, 1].tick_params(axis='x', rotation=45)

plt.tight_layout(rect=[0, 0, 1, 0.96])  # Leave space for suptitle

# Save figure to file
plt.savefig("../images/fayetteville_homeless_trends.png", dpi=300, bbox_inches='tight')

print("Plot saved as 'fayetteville_homeless_trends.png'")
