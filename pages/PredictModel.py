from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt


class PredictModel:
    def __init__(self, feature_range=(0, 100), cumulative_explained_variance=0.99):
        self.feature_range = feature_range
        self.cumulative_explained_variance = cumulative_explained_variance
        self.scaler = MinMaxScaler(feature_range=feature_range)
        self.pca = PCA()
        self.num_components = None

    def fit_and_predict_score(self, input_data):
        # Fit the scaler and PCA with the input data
        input_data = input_data.apply(np.cbrt)
        X_standardized = self.scaler.fit_transform(input_data)
        self.pca.fit(X_standardized)

        # Determine the number of components to include
        explained_variance_ratio = self.pca.explained_variance_ratio_
        self.num_components = np.argmax(np.cumsum(explained_variance_ratio) >= self.cumulative_explained_variance) + 1

        # Transform the data into principal component scores and select the top components
        principal_component_scores = self.pca.transform(X_standardized)
        digital_engagement_score = np.sum(principal_component_scores[:, :self.num_components], axis=1)
        print(digital_engagement_score)
        # Scale the scores
        scaled_scores = self.scaler.fit(digital_engagement_score.reshape(-1, 1))
        scaled_scores = self.scaler.transform(digital_engagement_score.reshape(-1, 1))

        return scaled_scores[-1][0]
    
    def generate_plot(self, input_data):
        input_data = input_data.apply(np.cbrt)
        X_standardized = self.scaler.fit_transform(input_data)

        columns = [f'Column {i}' for i in range(X_standardized.shape[1])]
        scaled_scores = self.scaler.transform(X_standardized)   
        
        # Create a bar plot
        plt.figure(figsize=(12, 6))
        plt.bar(columns, scaled_scores[:, 0])

        # Mark input values with stars
        input_values = X_standardized[-1]
        for i, val in enumerate(input_values):
            if val > 0:
                plt.plot(i, scaled_scores[-1][0], marker='*', markersize=10, color='red')

        plt.xlabel('Columns')
        plt.ylabel('Scaled Score')
        plt.title('Scaled Scores for Each Column')
        plt.xticks(rotation=45)

        # Save the plot as an image or display it
        # plt.savefig('score_plot.png')  # Uncomment this line to save the plot as an image
        # plt.show()  # Use this to display the plot

        return plt  # You can return the entire plot if you want to display it in your Dash app
