import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, plot_tree

# [Part 1 & 2: Classification Tree Comparison]
# ID3/C4.5 (Entropy) vs CART (Gini Index)

# Load Dataset
iris = load_iris()
X = iris.data[:, 2:] # Use Petal length and width for visualization
y = iris.target

# 1. ID3/C4.5 Style (Using Entropy)
# Note: scikit-learn implements a version of CART that supports both Gini and Entropy.
# It performs binary splits even with entropy.
tree_entropy = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=42)
tree_entropy.fit(X, y)

# 2. CART Style (Using Gini Index)
tree_gini = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=42)
tree_gini.fit(X, y)

# Visualization 1: Tree Structures
fig1, axes1 = plt.subplots(nrows=1, ncols=2, figsize=(20, 8))

# Entropy Tree
plot_tree(tree_entropy, filled=True, feature_names=iris.feature_names[2:],
          class_names=iris.target_names, ax=axes1[0])
axes1[0].set_title("Entropy-based Tree (ID3/C4.5 Concept)", fontsize=16)

# Gini Tree
plot_tree(tree_gini, filled=True, feature_names=iris.feature_names[2:],
          class_names=iris.target_names, ax=axes1[1])
axes1[1].set_title("Gini-based Tree (Standard CART)", fontsize=16)

plt.tight_layout()
plt.show()