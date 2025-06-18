import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from sklearn.model_selection import train_test_split
from scipy.sparse import coo_matrix, csr_matrix
from scipy.spatial.distance import jaccard, cosine
from collections import namedtuple

# Define the data structure
Data = namedtuple('Data', ['users', 'movies', 'train', 'test'])

class RecSys():
    def __init__(self, data):
        self.data = data
        self.allusers = list(self.data.users['uID'])
        self.allmovies = list(self.data.movies['mID'])
        self.genres = list(self.data.movies.columns.drop(['mID', 'title', 'year']))
        self.mid2idx = dict(zip(self.data.movies.mID, list(range(len(self.data.movies)))))
        self.uid2idx = dict(zip(self.data.users.uID, list(range(len(self.data.users)))))
        self.Mr = self.rating_matrix()
        self.Mm = None 
        self.sim = np.zeros((len(self.allmovies), len(self.allmovies)))
        
    def rating_matrix(self):
        """
        Convert the rating matrix to numpy array of shape (#allusers,#allmovies)
        """
        ind_movie = [self.mid2idx[x] for x in self.data.train.mID] 
        ind_user = [self.uid2idx[x] for x in self.data.train.uID]
        rating_train = list(self.data.train.rating)
        
        return np.array(coo_matrix((rating_train, (ind_user, ind_movie)), 
                                 shape=(len(self.allusers), len(self.allmovies))).toarray())

    def predict_everything_to_3(self):
        """
        Predict everything to 3 for the test data
        """
        return np.full(len(self.data.test), 3)
        
    def predict_to_user_average(self):
        """
        Predict to average rating for the user.
        Returns numpy array of shape (#users,)
        """
        # Calculate average rating for each user
        user_ratings = self.Mr
        user_avg = np.zeros(len(self.allusers))
        
        for i in range(len(self.allusers)):
            # Get non-zero ratings for this user
            user_ratings_i = user_ratings[i][user_ratings[i] > 0]
            if len(user_ratings_i) > 0:
                user_avg[i] = np.mean(user_ratings_i)
            else:
                user_avg[i] = 3  # Default to 3 if no ratings
        
        return user_avg
    
    def predict_from_sim(self, uid, mid):
        """
        Predict a user rating on a movie given userID and movieID
        """
        # Get user index and movie index
        u_idx = self.uid2idx[uid]
        m_idx = self.mid2idx[mid]
        
        # Get user's ratings and movie similarities
        user_ratings = self.Mr[u_idx]
        movie_similarities = self.sim[m_idx]
        
        # Get indices of movies the user has rated
        rated_movies = np.where(user_ratings > 0)[0]
        
        if len(rated_movies) == 0:
            return 3  # Default prediction if user hasn't rated any movies
        
        # Calculate weighted average of ratings based on similarities
        numerator = np.sum(user_ratings[rated_movies] * movie_similarities[rated_movies])
        denominator = np.sum(np.abs(movie_similarities[rated_movies]))
        
        if denominator == 0:
            return 3  # Default prediction if no valid similarities
        
        return numerator / denominator
    
    def predict(self):
        """
        Predict ratings in the test data. Returns predicted rating in a numpy array of size (# of rows in testdata,)
        """
        predictions = np.zeros(len(self.data.test))
        
        for i, (_, row) in enumerate(self.data.test.iterrows()):
            predictions[i] = self.predict_from_sim(row['uID'], row['mID'])
        
        return predictions
    
    def rmse(self, yp):
        yp[np.isnan(yp)] = 3  # In case there is nan values in prediction, it will impute to 3
        yt = np.array(self.data.test.rating)
        return np.sqrt(((yt-yp)**2).mean())
    
class ContentBased(RecSys):
    def __init__(self, data):
        super().__init__(data)
        self.data = data
        self.Mm = self.calc_movie_feature_matrix()  
        
    def calc_movie_feature_matrix(self):
        """
        Create movie feature matrix in a numpy array of shape (#allmovies, #genres) 
        """
        # Convert genre columns to numpy array
        genre_matrix = self.data.movies[self.genres].values
        return genre_matrix
    
    def calc_item_item_similarity(self):
        """
        Create item-item similarity using Jaccard similarity
        """
        n_movies = len(self.allmovies)
        self.sim = np.zeros((n_movies, n_movies))
        
        for i in range(n_movies):
            for j in range(n_movies):
                # Calculate Jaccard similarity between movies i and j
                intersection = np.sum(np.logical_and(self.Mm[i], self.Mm[j]))
                union = np.sum(np.logical_or(self.Mm[i], self.Mm[j]))
                
                if union == 0:
                    self.sim[i, j] = 0
                else:
                    self.sim[i, j] = intersection / union
                
class Collaborative(RecSys):    
    def __init__(self, data):
        super().__init__(data)
        
    def calc_item_item_similarity(self, simfunction, *X):  
        """
        Create item-item similarity using similarity function. 
        X is an optional transformed matrix of Mr
        """    
        if len(X) == 0:
            self.sim = simfunction()            
        else:
            self.sim = simfunction(X[0])
            
    def cossim(self):    
        """
        Calculates item-item similarity for all pairs of items using cosine similarity
        Returns a cosine similarity matrix of size (#all movies, #all movies)
        """
        n_movies = len(self.allmovies)
        self.sim = np.zeros((n_movies, n_movies))
        
        for i in range(n_movies):
            for j in range(n_movies):
                # Get ratings for movies i and j
                ratings_i = self.Mr[:, i]
                ratings_j = self.Mr[:, j]
                
                # Calculate cosine similarity
                dot_product = np.dot(ratings_i, ratings_j)
                norm_i = np.sqrt(np.sum(ratings_i**2))
                norm_j = np.sqrt(np.sum(ratings_j**2))
                
                if norm_i == 0 or norm_j == 0:
                    self.sim[i, j] = 0
                else:
                    self.sim[i, j] = dot_product / (norm_i * norm_j)
        
        return self.sim
    
    def jacsim(self, Xr):
        """
        Calculates item-item similarity for all pairs of items using jaccard similarity
        Xr is the transformed rating matrix.
        """    
        n_movies = len(self.allmovies)
        self.sim = np.zeros((n_movies, n_movies))
        
        for i in range(n_movies):
            for j in range(n_movies):
                # Get ratings for movies i and j
                ratings_i = Xr[:, i]
                ratings_j = Xr[:, j]
                
                # Calculate Jaccard similarity
                intersection = np.sum(np.logical_and(ratings_i > 0, ratings_j > 0))
                union = np.sum(np.logical_or(ratings_i > 0, ratings_j > 0))
                
                if union == 0:
                    self.sim[i, j] = 0
                else:
                    self.sim[i, j] = intersection / union
        
        return self.sim

def main():
    # Load the data
    try:
        users = pd.read_csv('data/users.csv')
        movies = pd.read_csv('data/movies.csv')
        train = pd.read_csv('data/train.csv')
        test = pd.read_csv('data/test.csv')
        
        data = Data(users, movies, train, test)
        
        # Test the recommender systems
        print("\nTesting Recommender Systems...")
        
        # Test baseline predictions
        recsys = RecSys(data)
        print("\nBaseline RMSE (predict everything to 3):", 
              recsys.rmse(recsys.predict_everything_to_3()))
        print("User Average RMSE:", 
              recsys.rmse(recsys.predict_to_user_average()))
        
        # Test content-based filtering
        content_based = ContentBased(data)
        content_based.calc_item_item_similarity()
        print("\nContent-Based RMSE:", 
              content_based.rmse(content_based.predict()))
        
        # Test collaborative filtering
        collaborative = Collaborative(data)
        collaborative.calc_item_item_similarity(collaborative.cossim)
        print("\nCollaborative Filtering (Cosine) RMSE:", 
              collaborative.rmse(collaborative.predict()))
        
        # Test collaborative filtering with Jaccard similarity
        binary_ratings = (data.train.rating > 3).astype(int)
        collaborative.calc_item_item_similarity(collaborative.jacsim, binary_ratings)
        print("Collaborative Filtering (Jaccard) RMSE:", 
              collaborative.rmse(collaborative.predict()))
        
    except FileNotFoundError as e:
        print(f"Error: Could not find data file - {e}")
        print("Please ensure all data files are present in the 'data' directory:")
        print("- users.csv")
        print("- movies.csv")
        print("- train.csv")
        print("- test.csv")

if __name__ == "__main__":
    main() 