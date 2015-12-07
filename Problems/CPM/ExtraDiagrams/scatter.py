def plot_scatter(lista, listb, name, colora="Blue", colorb="Red"):
    import matplotlib.pyplot as plt

    # Create some data to plot
    x_lista = [l[0] for l in lista]
    y_lista = [l[1] for l in lista]

    x_listb = [l[0] for l in listb]
    y_listb = [l[1] for l in listb]

    # Create a Figure object.
    fig = plt.figure()

    # Create an Axes object.
    ax = fig.add_subplot(1,1,1) # one row, one column, first plot

    # Plot the data.
    ax.scatter(x_lista, y_lista, color=colora, marker="^")
    ax.scatter(x_listb, y_listb, color=colorb, marker=".")

    # Add a title.
    ax.set_title(name)
    # Add some axis labels.
    ax.set_xlabel("Projection on First Eigen vector (approximation)")
    ax.set_ylabel("Projection on Second Eigen vector (approximation)")
    # Produce an image.
    fig.savefig(name + ".png")
    print "here", name
