import seaborn as sns
import matplotlib.pyplot as plt 

def sns_plot_and_save(data, path='fig.png', invert_axis=True, **kwargs):
    """Plot a seaborn heatmap of 2d dataset and save to file.

    Args:
        data (2d array): data to be plotted
        path (str, optional): filepath to save plot to. Defaults to 'fig.png'.
        invert_axis (bool, optional): ax.invert_yaxis, often needed for southern hemisphere met data. Defaults to True.
    """
    fig, ax = plt.subplots()
    sns.heatmap(data, ax=ax, **kwargs)
    if invert_axis:
        ax.invert_yaxis()
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)

def hist_plot_and_save(data, path='fig.png', bins=50, **kwargs):
    """Plot a matplotlib histogram of data and save to file.

    Args:
        data (array): data to be plotted
        path (str, optional): filepath to save plot to. Defaults to 'fig.png'.
        bins (int, optional): number of histogram bins. Defaults to 50.
    """
    fig, ax = plt.subplots()
    ax.hist(data, bins=bins, **kwargs)
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)

def plt_plot_and_save(data, path='fig.png', **kwargs):
    """Ax.imshow plot of 2d data and save to file.

    Args:
        data (2d data): data to be plotted
        path (str, optional): filepath to save plot to. Defaults to 'fig.png'.
    """
    fig, ax = plt.subplots()
    ax.imshow(data, cmap="viridis", **kwargs)
    fig.savefig(path, bbox_inches='tight')
    plt.close(fig)