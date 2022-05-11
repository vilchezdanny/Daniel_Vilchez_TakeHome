import matplotlib.pyplot as plt
import matplotlib.style as style


# plot line chart from Series
def plot_line_chart(
    series, title, subtitle, x_label, y_label, x_text, y1_text, y2_text
):
    style.use("fivethirtyeight")
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(series)
    # Title
    ax.text(x=x_text, y=y1_text, s=title, fontsize=16, weight="bold")
    # Subtitle
    ax.text(x=x_text, y=y2_text, s=subtitle, fontsize=15)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.show()


def plot_scatter_plot(
    df, x_axis, y_axis, title, subtitle, x_label, y_label, x_text, y1_text, y2_text
):
    style.use("fivethirtyeight")
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df[x_axis], df[y_axis])
    # Title
    ax.text(x=x_text, y=y1_text, s=title, fontsize=16, weight="bold")
    # Subtitle
    ax.text(x=x_text, y=y2_text, s=subtitle, fontsize=15)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.show()


# plot histogram from Series
def plot_histogram(series, title, subtitle, x_label, y_label, x_text, y1_text, y2_text):
    style.use("fivethirtyeight")
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.hist(series)
    # Title
    ax.text(x=x_text, y=y1_text, s=title, fontsize=16, weight="bold")
    # Subtitle
    ax.text(x=x_text, y=y2_text, s=subtitle, fontsize=15)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()
