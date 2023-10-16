from typing import List

import pandas as pd
from abc import ABC, abstractmethod
from domain.entities.base import ClusterDTO, TransactionDTO, Cluster, Transaction
from domain.adapter import DataframeAdapter


class DataframeRepository(ABC):

    def __init__(self, adapter: DataframeAdapter) -> None:
        self.adapter = adapter

    @abstractmethod
    def get_dataframe(self) -> pd.DataFrame:
        pass


class ClusterRepository(DataframeRepository):

    def get_dataframe(self) -> pd.DataFrame:
        df = self.adapter.load_dataframe()
        # Convert from string to datetime
        df["Start Date"] = df["Start Date"].apply(pd.to_datetime)
        df["End Date"] = df["End Date"].apply(pd.to_datetime)

        return df


class TransactionRepository(DataframeRepository):
    """Transaction repository"""

    def get_dataframe(self) -> pd.DataFrame:
        """Get Transactions read from Excel file in dataframe format.
        Returns:
            pd.DataFrame: Transactions read from Excel file in dataframe format.
        """
        df = self.adapter.load_dataframe()
        # Convert from string to datetime
        df["Transaction Date"] = df["Transaction Date"].apply(pd.to_datetime)

        return df


class ClusterAggregateRepository:
    def __init__(self, cluster_repository: ClusterRepository, transaction_repository: TransactionRepository):
        """ Initialize the repository with the cluster and transaction repositories.
        Args:
            cluster_repository (ClusterRepository): Cluster repository.
            transaction_repository (TransactionRepository): Transaction repository.
        """
        self.cluster_repository = cluster_repository
        self.transaction_repository = transaction_repository
        self.cluster_transactions_df = self.merge_transactions_to_clusters()

    def merge_transactions_to_clusters(self) -> pd.DataFrame:
        clusters = self.cluster_repository.get_dataframe()
        transactions = self.transaction_repository.get_dataframe()

        # Right join clusters and transactions
        cluster_transactions = pd.merge(clusters["Cluster Id"], transactions, on="Cluster Id",  how="right")

        return cluster_transactions

    def get_cluster_transactions(self, cluster_id: str) -> List[Transaction]:
        """Get transactions for a specific cluster.
        Args:
            cluster_id (str): Cluster id.
        Returns:
            List[Transaction]: List of transactions for the specified cluster.
        """
        # Filter by cluster id
        cluster_transactions = self.cluster_transactions_df[self.cluster_transactions_df["Cluster Id"] == cluster_id]

        transaction_dto_list = [TransactionDTO.from_dict(t) for t in
                                cluster_transactions.to_dict(orient="records")]

        transaction_list = [Transaction.from_dto(t) for t in transaction_dto_list]

        return transaction_list

    def get_all_clusters(self) -> List[Cluster]:
        """Get all clusters and transactions joined together by cluster id.
        Returns:
            List[Cluster]: List of clusters and transactions joined together by cluster id.
        """

        clusters = self.cluster_repository.get_dataframe()

        cluster_list = []

        # Iterate over rows from clusters
        for _, cluster in clusters.iterrows():
            cluster_dto = ClusterDTO.from_dict(cluster.to_dict())
            cluster = Cluster.from_dto(cluster_dto)

            cluster.transactions = self.get_cluster_transactions(cluster.id)
            cluster_list.append(cluster)

        return cluster_list
