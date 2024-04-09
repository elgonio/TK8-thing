import os

plots_dir = 'plots'
os.makedirs(plots_dir, exist_ok=True)

import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

from enums import dan_names_dict

def plot_win_rates(win_rates, bracket_name='', ylim=(0.45, 0.7), date_range='unknown'):
    # plot the win rates with confidence intervals
    plt.figure(figsize=(10, 5))
    sns.barplot(x=list(win_rates.keys()), y=list(win_rates.values()))
    plt.title(f'Win Rates_{bracket_name}')
    plt.text(0.99, 1.05, date_range, verticalalignment='top', horizontalalignment='right', transform=plt.gca().transAxes)
    plt.xlabel('Character')
    plt.ylabel('Win Rate')
    plt.ylim(ylim[0], ylim[1])
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, f'win_rates_{bracket_name}.png'))
    plt.show()

def plot_win_rates_with_confidence_intervals(win_rates, confidence_intervals, bracket_name='', ylim=(0.45, 0.7), date_range='unknown'):
    # plot the win rates with confidence intervals
    plt.figure(figsize=(10, 5))
    sns.barplot(x=list(win_rates.keys()), y=list(win_rates.values()))
    for i in range(len(win_rates)):
        key = list(win_rates.keys())[i]
        win_rate = win_rates[key]
        lower_bound = confidence_intervals[key][0]
        upper_bound = confidence_intervals[key][1]
        plt.errorbar(i, win_rate, yerr=[[win_rate - lower_bound], [upper_bound-win_rate]], capsize=5, color='black')
    plt.title(f'Win Rates with 95% Confidence Intervals_{bracket_name}')
    plt.text(0.99, 1.05, date_range, verticalalignment='top', horizontalalignment='right', transform=plt.gca().transAxes)
    plt.xlabel('Character')
    plt.ylabel('Win Rate')
    plt.ylim(ylim[0], ylim[1])
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, f'win_rates_with_confidence_intervals_{bracket_name}.png'))
    plt.show()

def plot_most_popular_characters(character_counts, bracket_name='', date_range='unknown'):
    # plot the most popular characters
    character_counts = Counter(character_counts)
    character_counts = dict(character_counts)
    character_counts = {k: v for k, v in sorted(character_counts.items(), key=lambda item: item[1], reverse=True)}
    plt.figure(figsize=(10, 5))
    sns.barplot(x=list(character_counts.keys()), y=list(character_counts.values()))
    plt.title(f'Most Popular Characters_{bracket_name}')
    plt.text(0.99, 1.05, date_range, verticalalignment='top', horizontalalignment='right', transform=plt.gca().transAxes)
    plt.xlabel('Character')
    plt.ylabel('Count')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, f'most_popular_characters_{bracket_name}.png'))
    plt.show()

def plot_rank_distribution(rank_counts, date_range='unknown'):
    # plot the rank distribution
    rank_counts = Counter(rank_counts)
    rank_counts = dict(rank_counts)
    rank_counts = {f'{dan_names_dict[k]} ({k})': v for k, v in sorted(rank_counts.items(), key=lambda item: item[0], reverse=False)}
    plt.figure(figsize=(10, 5))
    sns.barplot(x=list(rank_counts.keys()), y=list(rank_counts.values()))
    plt.title('Rank Distribution')
    plt.text(0.99, 1.05, date_range, verticalalignment='top', horizontalalignment='right', transform=plt.gca().transAxes)
    plt.xlabel('Rank')
    plt.ylabel('Count')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, 'rank_distribution.png'))
    plt.show()
