import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Use Pandas to import the data from "fcc-forum-pageviews.csv" and set the index to the date column
# Replace 'fcc-forum-pageviews.csv' with the actual filename or path to your dataset
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean the data by filtering out days when the page views were in the top 2.5% or bottom 2.5% of the dataset
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]

# Create a draw_line_plot function that uses Matplotlib to draw a line chart
def draw_line_plot():
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df.index, df['value'], color='r', linewidth=1)
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xticks(rotation=45)
    plt.savefig('line_plot.png')
    return plt.gca()

# Create a draw_bar_plot function that draws a bar chart
def draw_bar_plot():
    df_bar = df.groupby([df.index.year, df.index.month]).mean().unstack()
    df_bar.index.names = ['Years', 'Months']
    df_bar.columns = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    ax = df_bar.plot(kind='bar', figsize=(15, 10))
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.title('Average Daily Page Views for Each Month (Year-wise)')
    plt.legend(title='Months', labels=df_bar.columns.map(str))
    plt.savefig('bar_plot.png')
    return plt.gca()

# Create a draw_box_plot function that uses Seaborn to draw two adjacent box plots
def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    fig, axes = plt.subplots(1, 2, figsize=(24, 10))
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    axes[0].set_title('Year-wise Box Plot (Trend)')

    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    axes[1].set_title('Month-wise Box Plot (Seasonality)')

    plt.savefig('box_plot.png')
    return plt.gca()

# Run the functions and save the images
draw_line_plot()
draw_bar_plot()
draw_box_plot()
