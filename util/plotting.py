import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.pyplot 
import pandas as pd

def plot_bar(df, filename=None, weight='charges_share', disagg=True, xlab="Mean charge (USD)"):
    """
    Plots a bar chart of insurer charges based on the provided dataframe and parameters.

    Parameters:
    - df: The dataframe containing the data to be plotted.
    - filename: The name of the file to save the plot. If None, the plot will not be saved.
    - weight: The column used to weight the insurer charges. Default is 'charges_share'.
    - disagg: A boolean indicating whether the data should be disaggregated. Default is True.
    - xlab: The label for the x-axis. Default is "Mean charge (USD)".
    """

    # ~~~~~~~~ Prepare data ~~~~~~~~~~
    if weight is None:
        if not disagg:
            df = df.groupby(['insurer']).agg({'insurer_charge':'mean'}).reset_index().sort_values('insurer_charge')
        else:
            df = df.groupby(['insurer','type']).agg({'insurer_charge':'mean'}).reset_index().sort_values(['insurer_charge'])

    else:
        df['insurer_charge'] = df['insurer_charge'] * df[weight]
        if not disagg:
            df = df.groupby(['insurer']).agg({'insurer_charge':'sum'}).reset_index().sort_values('insurer_charge')
        else:
            df = df.groupby(['insurer','type']).agg({'insurer_charge':'sum'}).reset_index().sort_values(['insurer_charge'])

        
    # ~~~~~~~~ Plot ~~~~~~~~
            
    # Set figure metadata
    sns.set(font='Times New Roman')
    sns.set_theme(style="whitegrid")
    sns.set_color_codes("colorblind")
    plt.figure(figsize=(12, 8))
    ax = plt.gca()

    if  disagg:
        sns.barplot(df, x='insurer_charge', y='insurer', hue='type', orient='h', errorbar='sd')
    else:
        sns.barplot(df, x='insurer_charge', y='insurer', orient='h', errorbar='sd', color='b')

    # Axes and legends
    ax.legend(ncol=2, loc="upper right", frameon=True)
    ax.set(ylabel="",
       xlabel=xlab)
    sns.despine(left=True, bottom=True)

    # Save figure
    plt.savefig(filename, bbox_inches='tight')
    print("Saved figure to " + filename)