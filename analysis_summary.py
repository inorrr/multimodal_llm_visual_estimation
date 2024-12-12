import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from tabulate import tabulate

gpt4_evaluation = "results/gpt4_evaluation.csv"
true_count = "FSC147_384_V2/300_image_labels.csv"
human_data = "results/human_evaluation.csv"

true_data = pd.read_csv(true_count)
human_data = pd.read_csv(human_data)
gpt_data = pd.read_csv(gpt4_evaluation)

def true_count_boxplot():
    plt.figure(figsize=(10, 4))  # Adjust the figure size as needed
    plt.boxplot(true_data['object_count'], patch_artist=True, vert=False)  # Create a boxplot

    plt.title('Distribution of the Ture Object Count')
    plt.xlabel('Object Count')
    plt.grid(True)
    plt.savefig('plots/true_count_boxplot.png', format='png', dpi=300)  # Specify the path, format, and DPI
    plt.show()


def scatter_plot():

    df = true_data
    fig, ax = plt.subplots(figsize=(12, 4))
    classes = pd.Categorical(df['class'])
    df['class_code'] = classes.codes

    scatter = ax.scatter(df['class_code'], df['object_count'], c=df['object_count'], cmap='viridis', alpha=0.6, edgecolors='w', linewidths=0.5)

    # Customizing the ticks on the X-axis to show class names instead of codes
    ax.set_xticks(range(len(classes.categories)))
    ax.set_xticklabels(classes.categories, rotation=45, ha='right', fontsize=5)

    # Adding labels and title
    ax.set_xlabel('Class')
    ax.set_ylabel('Object Count')
    ax.set_title('Scatter Plot of Object Counts by Class')

    # Adding a horizontal color bar
    cbar = plt.colorbar(scatter, orientation='vertical')

    plt.show()


def human_performance():

    df = human_data
    df = df[df['object_count'] <= 800]
    # Create a scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(df['object_count'], df['human'], color='blue', alpha=0.6, edgecolor='black')

    # Add a line of perfect agreement
    plt.plot([min(df['object_count']), max(df['object_count'])], [min(df['object_count']), max(df['object_count'])], color='red', linestyle='--')

    # Labeling the plot
    plt.xlabel('True Count')
    plt.ylabel('Human Count')
    plt.title('Comparison of Human Count vs. True Count')
    plt.grid(True)

    # Add annotations for clarity
    # for i, row in df.iterrows():
    #     plt.annotate(row['filename'], (row['object_count'] + 0.5, row['human']), textcoords="offset points", xytext=(0,10), ha='center')

    plt.show()

def gpt_performance():

    df = gpt_data
    human_df=human_data
    # Create a scatter plot
    marker_size = 20  # Adjust this value as needed, smaller numbers mean smaller dots
    plt.figure(figsize=(8, 6))

    plt.scatter(human_df['object_count'], human_df['human'], color='orange', alpha=0.5, s=marker_size, label='Human')
    plt.scatter(df['object_count'], df['gpt_4_initial_answer'], color='blue', alpha=0.3, s=marker_size, label='GPT4: Vanilla ')
    plt.scatter(df['object_count'], df['response_desc_true_direct_true_indirect_true'], color='green', alpha=0.3, s=marker_size, label='GPT4: all info')
    # plt.scatter(df['object_count'], df['response_desc_true_direct_false_indirect_false'], color='red', alpha=0.3, s=marker_size, label='GPT4: Description Only')
    # plt.scatter(df['object_count'], df['response_desc_false_direct_true_indirect_false'], color='yellow', alpha=0.3, s=marker_size, label='GPT4: Direct Hint Only')
    # plt.scatter(df['object_count'], df['response_desc_false_direct_false_indirect_true'], color='pink', alpha=0.3, s=marker_size, label='GPT4: Indirect Hint Only')

    # Add a line of perfect agreement
    plt.plot([min(df['object_count']), max(df['object_count'])], [min(df['object_count']), max(df['object_count'])], color='red', linestyle='--')

    # Labeling the plot
    plt.xlabel('True Count')
    plt.ylabel('GPT4 Count')
    plt.title('Comparison of GPT4 Performance with Different Side Information')
    plt.grid(True)
    plt.legend()  # This will display the legend

    plt.show()

def count_size():
 
    count1 = (true_data['object_count'] < 20).sum()
    count2 = ((true_data['object_count'] >= 20) & (true_data['object_count'] < 100)).sum()
    count3 = (true_data['object_count'] >= 100).sum()
    print("Count 1 (object_count < 20):", count1)
    print("Count 2 (20 <= object_count < 100):", count2)
    print("Count 3 (object_count >= 100):", count3) 

    unique_categories = true_data['class'].nunique()
    print("Number of unique categories:", unique_categories)

    mean_count = true_data['object_count'].mean()
    print(f"Mean of object_count: {mean_count}")

    min_count = true_data['object_count'].min()
    max_count = true_data['object_count'].max()
    count_range = max_count - min_count
    print(f"Minimum count: {min_count}")
    print(f"Maximum count: {max_count}")
    print(f"Range of count: {count_range}")


def csv_to_latex():
    csv_path = "results/rmse_evaluation.csv"
    df = pd.read_csv(csv_path)  

    latex_table = tabulate(df, tablefmt="latex", headers="keys", showindex="never")
    
    output_file_path = 'results/rmse_latex.txt'

    with open(output_file_path, 'w') as file:
        file.write(latex_table)
    print(f"LaTeX table has been saved to {output_file_path}")


def main():
    # true_count_boxplot()
    # scatter_plot()
    # human_performance()
    gpt_performance()
    # count_size()
    # csv_to_latex()

if __name__ == "__main__":
    main()