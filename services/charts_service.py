import matplotlib.pyplot as plt
import pandas as pd

def generate_bar_chart(df, column, filename, x=None):
    plt.figure()
    if x:
        plt.bar(df[x], df[column])
        plt.xlabel(x)
    else:
        plt.bar(df.index, df[column])
        plt.xlabel('Index')
    plt.ylabel(column)
    plt.title('Wykres słupkowy')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def generate_line_chart(df, columns, filename, x=None):
    plt.figure()
    for col in columns:
        if x:
            plt.plot(df[x], df[col], label=col)
        else:
            plt.plot(df[col], label=col)
    plt.legend()
    plt.xlabel(x if x else 'Index')
    plt.ylabel('Wartość')
    plt.title('Wykres liniowy')
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def generate_pie_chart(df, column, filename):
    plt.figure()
    df[column].value_counts().plot(kind='pie')
    plt.savefig(filename)
    plt.close()
