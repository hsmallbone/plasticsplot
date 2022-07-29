import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mc
import matplotlib.cm as cm
import matplotlib.colorbar as cb
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

global_colors = {
    'green': (0.36, 0.8, 0.7, 0.9),
    'red': (0, 0.77, 0.8, 1),
    'grey': (0, 0, 0.25, 0.5)
}


def gen_colors(name, n):
    colors = []
    base = global_colors[name]
    for i in range(n):
        colors.append(mc.hsv_to_rgb((base[0], base[1], base[2] + (base[3] - base[2]) * i / n)))
    colors.reverse()
    return mc.ListedColormap(colors=colors)


def plot_colorbar(ax, name, loc, offset):
    cbaxes = inset_axes(plt.gca(), width="20%", height="3%", loc=loc, bbox_to_anchor=offset,
                        bbox_transform=ax.transAxes)
    norm = mc.Normalize(vmin=0, vmax=1)
    cbar = cb.ColorbarBase(cbaxes, cmap=gen_colors(name, 5), norm=norm,
                           orientation='horizontal')
    cbar.ax.set_xticklabels(['Mild', '', 'Severe'])


def get_pos(idx, v, n):
    rads = 2 * 3.14 / n
    return ((-idx * rads) - (rads / 2), v, rads)


def get_col(base, v, max=None):
    if isinstance(base, str):
        base = global_colors[base]
        max = base[3]
    return mc.hsv_to_rgb((base[0], base[1], base[2] + v * (max - base[2])))


def make_plot(title=None, ticks=None, bars=None, draw_arrows=False):
    if ticks is None:
        ticks = [0.15, 0.3, 0.45]
    if title is None:
        title = [['Reduction Mammoplasty Risk Profile', 'red'],
                 ['Everyday Risk Comparison', 'gray'],
                 ['Breast-Q Outcomes', 'green']]
    if bars is None:
        bars = [
            {
                'label': 'Test sentence (50%)',
                'color': 'green',
                'value': 0.5,
                'color_value': 0.9
            },
            {
                'label': 'Test2 (40%)',
                'color': 'red',
                'value': 0.4,
                'color_value': 0.6
            },
            {
                'label': 'Test3 (30%)',
                'color': 'grey',
                'value': 0.3,
                'color_value': 0.45
            },
            {
                'label': 'Test4 (20%)',
                'color': 'grey',
                'value': 0.2,
                'color_value': 0.3
            },
            {
                'label': 'Test5 (15%)',
                'color': 'green',
                'value': 0.15,
                'color_value': 0.2
            },
            {
                'label': 'Test6 (15%)',
                'color': 'red',
                'value': 0.12,
                'color_value': 0.5
            },
            {
                'label': 'Test6 but \nlong txt (10%)',
                'color': 'green',
                'value': 0.1,
                'color_value': 0.4
            },
            {
                'label': 'Test7 but \nlong txt (8%)',
                'color': 'grey',
                'value': 0.08,
                'color_value': 0.2
            },
            {
                'label': 'Test9 but (8%)',
                'color': 'green',
                'value': 0.08,
                'color_value': 0.2
            },
            {
                'label': 'Test10 but (8%)',
                'color': 'green',
                'value': 0.08,
                'color_value': 0.2
            },
            {
                'label': 'Test11 but \nlong txt(8%)',
                'color': 'grey',
                'value': 0.08,
                'color_value': 0.2
            },
        ]
    bars = list(sorted(bars, key=lambda item: -item['value']))
    fig = plt.figure()
    fig.set_size_inches(7, 6, forward=True)

    ax = plt.subplot(projection='polar')

    ax.set_theta_zero_location('N')
    ax.spines['polar'].set_visible(False)
    ax.set_rlabel_position(ax.get_rlabel_position() - 17)

    ax.yaxis.grid(linewidth=0.5, linestyle=(0, (5, 5)))
    ax.xaxis.grid(linewidth=0)

    ax.set_xticklabels([])
    ax.set_yticks(ticks)
    ax.set_yticklabels([])

    tick_labels = [str(int(t * 100)) + '%' for t in ticks]
    for i, t in enumerate(ticks):
        ax.annotate(tick_labels[i], (124, 190 + 42 * i), xycoords='axes points')

    for i, line in enumerate(title):
        fig.text(0.15, 0.95 - i * 0.035, line[0], ha='left', va='bottom', size='large', color=line[1])

    plot_colorbar(ax, 'green', 'lower left', (-0.15, 0.04, 1, 1))
    plot_colorbar(ax, 'red', 'lower right', (0.15, 0.04, 1, 1))

    def plot(position, label, color, draw_arrows=False):
        import textwrap
        label = '\n'.join(textwrap.wrap(label, 15))
        r = ax.bar(position[0], position[1], width=position[2], color=color, bottom=0)
        rads = abs(position[0])
        ax.annotate(label, (position[0], position[1]), xytext=(
            3.14 * 2 - rads + (
                0.1 if rads < 1 else -0.1 if rads < 3 else -0.2 if rads < 4.32 else 0.1 if rads < 5.5 else 0.4),
            min(position[1] + 0.35, 0.51)),
                    textcoords='data',
                    bbox=dict(facecolor=np.append(color, 0.6), edgecolor='none', boxstyle='round,pad=0.5'),
                    arrowprops=dict(arrowstyle='->', color='black') if draw_arrows and rads > 2 else None)

    n = len(bars)
    for i, bar in enumerate(bars):
        plot(get_pos(i, bar['value'], n), bar['label'], get_col(bar['color'], bar['color_value']), draw_arrows)

    ax.set_position([0, -0, 1, 0.85])


def main(args=None):
    if args is None:
        args = dict()
    make_plot(args.get('title', None), args.get('ticks', None), args.get('bars', None), args.get('draw_arrows', False))
    plt.show()


if __name__ == '__main__':
    main()
# plt.tight_layout()
# plt.savefig('out.png')
