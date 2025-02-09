import seaborn as sns
import matplotlib.pyplot as plt 

def sns_plot_and_save(data, path='fig.png', invert_axis=True, **kwargs):
    fig, ax = plt.subplots()
    sns.heatmap(data, ax=ax, **kwargs)
    if invert_axis:
        ax.invert_yaxis()
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)

def hist_plot_and_save(data, path='fig.png', bins=50, **kwargs):
    fig, ax = plt.subplots()
    ax.hist(data, bins=bins, **kwargs)
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)

def plt_plot_and_save(data, path='fig.png', **kwargs):
    fig, ax = plt.subplots()
    ax.imshow(data, cmap="viridis", **kwargs)
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)