import sys
import pickle
sys.path.append("/Users/anjianli/Desktop/robotics/project/optimized_dp")

import numpy as np
import math
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

from prediction.process_prediction_v3 import *

class ClusteringV3(object):
    """
    Given cleaned data, we first normalize the acc and omega

    Then we set several default driving mode, and then cluster the variance

    """

    def __init__(self):

        self.to_plot = True

        self.clustering_num = 7

        # Clustering feature selection
        # self.clustering_feature_type = "5_default_deviation"
        # self.clustering_feature_type = "5_default_distance"
        self.clustering_feature_type = "only_mean"
        # self.clustering_feature_type = "mean_and_variance"

        # Default driving mode
        # Decelerate
        self.default_m1_acc = -1.5
        self.default_m1_omega = 0
        # Maintain
        self.default_m2_acc = 0
        self.default_m2_omega = 0
        # Turn Left
        self.default_m3_acc = 0.5
        self.default_m3_omega = 0.25
        # Turn right
        self.default_m4_acc = 0.5
        self.default_m4_omega = - 0.25
        # Accelerate
        self.default_m5_acc = 1.3
        self.default_m5_omega = 0
        # Curve path left
        self.default_m6_acc = 0.7
        self.default_m6_omega = 0.1
        # Curve path right
        self.default_m7_acc = 0.7
        self.default_m7_omega = - 0.1

        self.time_span = ProcessPredictionV3().mode_time_span

        # For plot comparison
        if ProcessPredictionV3().scenario_to_use == ["intersection", "roundabout"]:
            self.scenario_name = "intersection+roundabout"
        elif ProcessPredictionV3().scenario_to_use == ["intersection"]:
            self.scenario_name = "intersection"
        elif ProcessPredictionV3().scenario_to_use == ["roundabout"]:
            self.scenario_name = "roundabout"

        if ProcessPredictionV3().use_velocity:
            self.use_velocity = "use velocity"
        else:
            self.use_velocity = "only poly"

    def get_clustering(self):

        # The action feature vector is [acc_mean, acc_variance, omega_mean, omega_variance]
        action_feature = self.get_action_feature()

        # Form clustering feature from action feature
        clustering_feature = self.get_clustering_feature(action_feature)

        # Kmeans on clustering feature
        prediction = self.kmeans_clustering(clustering_feature)

        # Visualization
        self.plot_clustering(action_feature, clustering_feature, prediction)

        # Find the action bound for each mode
        mode_action_bound = self.get_action_bound_for_mode(prediction, action_feature)

    def get_action_feature(self):

        filename_action_feature_list = ProcessPredictionV3().collect_action_from_group()

        # Concatenate all the actions feature in a big list
        action_feature_list = []

        num_action_feature = 0
        for action_feature in filename_action_feature_list:
            for i in range(np.shape(action_feature[1])[0]):
                # The action feature vector is [acc_mean, acc_variance, omega_mean, omega_variance]
                action_feature_list.append([action_feature[1][i], action_feature[2][i], action_feature[3][i], action_feature[4][i]])
                num_action_feature += 1

        action_feature_list = np.asarray(action_feature_list)
        print("total number of action feature is ", num_action_feature)

        return action_feature_list

    def get_clustering_feature(self, action_feature):

        # action_feature = [acc_mean, acc_variance, omega_mean, omega_variance]
        if self.clustering_feature_type == "5_default_deviation":
            clustering_feature = np.transpose(np.asarray([
                action_feature[:, 0] - self.default_m1_acc, action_feature[:, 0] - self.default_m2_acc,
                action_feature[:, 0] - self.default_m3_acc, action_feature[:, 0] - self.default_m4_acc,
                action_feature[:, 0] - self.default_m5_acc,
                action_feature[:, 2] - self.default_m1_omega, action_feature[:, 2] - self.default_m2_omega,
                action_feature[:, 2] - self.default_m3_omega, action_feature[:, 2] - self.default_m4_omega,
                action_feature[:, 2] - self.default_m5_omega
            ]))
        elif self.clustering_feature_type == "5_default_distance":
            clustering_feature = np.transpose(np.asarray([
                np.sqrt((action_feature[:, 0] - self.default_m1_acc) ** 2 + (
                            action_feature[:, 2] - self.default_m1_omega) ** 2),
                np.sqrt((action_feature[:, 0] - self.default_m2_acc) ** 2 + (
                            action_feature[:, 2] - self.default_m2_omega) ** 2),
                np.sqrt((action_feature[:, 0] - self.default_m3_acc) ** 2 + (
                            action_feature[:, 2] - self.default_m3_omega) ** 2),
                np.sqrt((action_feature[:, 0] - self.default_m4_acc) ** 2 + (
                            action_feature[:, 2] - self.default_m4_omega) ** 2),
                np.sqrt((action_feature[:, 0] - self.default_m5_acc) ** 2 + (
                            action_feature[:, 2] - self.default_m5_omega) ** 2),
            ]))
        elif self.clustering_feature_type == "only_mean":
            clustering_feature = np.transpose(np.asarray([action_feature[:, 0], action_feature[:, 2]]))
        elif self.clustering_feature_type == "mean_and_variance":
            clustering_feature = np.transpose(np.asarray([action_feature[:, 0], action_feature[:, 2],
                                                          action_feature[:, 1], action_feature[:, 3]]))

        normalized_clustering_feature = MinMaxScaler().fit_transform(clustering_feature)

        return normalized_clustering_feature

    def kmeans_clustering(self, clustering_feature):

        default_centroid = np.asarray([[self.default_m1_acc, self.default_m1_omega],
                                       [self.default_m2_acc, self.default_m2_omega],
                                       [self.default_m3_acc, self.default_m3_omega],
                                       [self.default_m4_acc, self.default_m4_omega],
                                       [self.default_m5_acc, self.default_m5_omega],
                                       [self.default_m6_acc, self.default_m6_omega],
                                       [self.default_m7_acc, self.default_m7_omega]
                                       ])

        # kmeans_action = KMeans(n_clusters=self.clustering_num, random_state=0).fit(clustering_feature)
        kmeans_action = KMeans(n_clusters=self.clustering_num, init=default_centroid, n_init=10, max_iter=300).fit(clustering_feature)
        pred = kmeans_action.predict(clustering_feature)

        return pred

    def plot_clustering(self, original_data, clustering_data, prediction):

        fig, ax = plt.subplots()
        for i in range(self.clustering_num):
            ax.scatter(original_data[:, 0][prediction == i], original_data[:, 2][prediction == i], label='Cluster %d' % i)
        ax.set_xlabel('acceleration')
        ax.set_ylabel('angular_speed')
        title = self.use_velocity + ", " + self.scenario_name + ", " + self.clustering_feature_type + ", " + str(self.time_span) + " " + "time-span"
        ax.set_title(title)
        ax.legend()
        if self.to_plot:
            plt.show()

        # pickle.dump(kmeans_action, open("/home/anjianl/Desktop/project/optimized_dp/model/kmeans_action_intersection"
        #                                 ".pkl", "wb"))

    def get_action_bound_for_mode(self, prediction, action_feature):

        mode_num = np.max(prediction) + 1
        action_num = np.shape(prediction)[0]

        mode_action_bound = []

        for mode in range(mode_num):
            acc_min = np.min(action_feature[prediction == mode, 0])
            acc_max = np.max(action_feature[prediction == mode, 0])
            omega_min = np.min(action_feature[prediction == mode, 2])
            omega_max = np.max(action_feature[prediction == mode, 2])

            print("Mode {:d}: acc is in [{:.2f}, {:.2f}], omega is in [{:.2f}, {:.2f}]".format(mode, acc_min, acc_max, omega_min, omega_max))
            mode_action_bound.append([mode, acc_min, acc_max, omega_min, omega_max])

        return mode_action_bound

if __name__ == "__main__":
    ClusteringV3().get_clustering()