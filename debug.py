import seaborn as sns
import matplotlib.pyplot as plt 

def sns_plot_and_save(data, path='fig.png'):
    fig, ax = plt.subplots()
    sns.heatmap(data, ax=ax)
    fig.savefig(path)
    plt.close(fig)

def hist_plot_and_save(data, path='fig.png',  bins=50):
    fig, ax = plt.subplots()
    ax.hist(data, bins=bins)
    fig.savefig(path)
    plt.close(fig)