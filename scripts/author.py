import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import accumulate


def plot_curve(df, author_name):
    author_df = df.loc[df['author'] == author_name]
    year_frequencies = []
    unique_years = np.sort(list(set(author_df['ed_year'].astype(int))))

    for year in unique_years:
        year_df = author_df.loc[df['ed_year'] == year]
        year_frequencies.append(len(year_df))
    
    year_frequencies = list(accumulate(year_frequencies))

    plt.plot(unique_years, year_frequencies, marker='o', label=author_name)


def main():
    df = pd.read_csv('toc.csv')
    top_10_authors = df['author'].value_counts().head(10)

    plt.figure(figsize=(10, 6))
    plt.xlabel("Tid")
    plt.ylabel("Omnämnda")

    # Set y-axis limits
    plt.ylim(0, 90)

    # Set x-axis limits
    plt.xlim(1932, 2004)
    
    for author in top_10_authors.index:
        plot_curve(df, author)

    plt.legend()
    plt.tight_layout()

    # Display the plot
    #plt.show()

    plt.savefig("authors_top_10.png", dpi=400)

if __name__ == '__main__':
    main()
