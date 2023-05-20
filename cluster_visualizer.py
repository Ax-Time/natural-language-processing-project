import pickle
import numpy as np
from nltk import Counter

def load_data():
# Load the embeddings
    with open('dumps/sentence_clustering/embeddings.pkl', 'rb') as f:
        embeddings = np.array(pickle.load(f)).mean(axis=1)

    # Load the clusters
    with open('dumps/sentence_clustering/kmeans.pkl', 'rb') as f:
        kmeans = pickle.load(f)

    # Load the topics
    with open('dumps/sentence_clustering/topics.pkl', 'rb') as f:
        topics = np.array(pickle.load(f))
    return embeddings, kmeans, topics

embeddings, kmeans, topics = load_data()

# Perform PCA on the embeddings
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
pca.fit(embeddings)
embeddings_pca = pca.transform(embeddings)

# Create a tkinter window with a canvas to plot matplotlib figures
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
root = tk.Tk()
root.wm_title("Embedding Visualizer")

# Create a matplotlib figure
fig = Figure(figsize=(10, 10))
ax = fig.add_subplot(111)

# Add a slider
from tkinter import ttk
slider = ttk.Scale(root, from_=0, to=kmeans.n_clusters-1, orient='horizontal')
slider.pack(side='bottom', fill='x', padx=10, pady=10)

# Create a function to update the plot
def update_plot(event):
    # Get the slider value
    k = int(slider.get())

    # Clear the plot
    ax.clear()

    ax.set_title(f'Visualizing Cluster {k}')

    # Plot the embeddings of the cluster k in red and the others in blue
    ax.scatter(embeddings_pca[kmeans.labels_ == k, 0], embeddings_pca[kmeans.labels_ == k, 1], c='r', alpha=1)
    ax.scatter(embeddings_pca[kmeans.labels_ != k, 0], embeddings_pca[kmeans.labels_ != k, 1], c='b', alpha=0.05)

    # Write the topics of cluster k
    topics_k = topics[kmeans.labels_ == k]
    counter = Counter(topics_k)
    counter = ', '.join([f'{k}: {v}' for k, v in counter.items()])
    ax.text(0.05, 0.95, str(counter), transform=ax.transAxes, fontsize=14, verticalalignment='top')
    # Update the plot
    canvas.draw()

# Bind the slider to the update_plot function
slider.bind("<ButtonRelease-1>", update_plot)

# Create a canvas to draw the plot
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

# Start the GUI
k=1
update_plot(None)
tk.mainloop()