import seaborn as sns
import matplotlib.pyplot as plt 

def sns_plot_and_save(data, path='fig.png'):
    fig, ax = plt.subplots()
    sns.heatmap(data, ax=ax)
    ax.invert_yaxis()
    fig.savefig(path)
    plt.close(fig)

def hist_plot_and_save(data, path='fig.png',  bins=50):
    fig, ax = plt.subplots()
    ax.hist(data, bins=bins)
    fig.savefig(path)
    plt.close(fig)

def plt_plot_and_save(data, path='fig.png'):
    fig, ax = plt.subplots()
    ax.imshow(data, cmap="viridis")
    fig.savefig(path)
    plt.close(fig)