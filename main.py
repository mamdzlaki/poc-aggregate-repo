import os
from domain.repository import ClusterAggregateRepository, ClusterRepository, TransactionRepository
from domain.adapter import ExcelAdapter


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    cluster_file = os.path.join(ROOT_DIR, "tests/data/clusters.xlsx")
    transaction_file = os.path.join(ROOT_DIR, "tests/data/transactions.xlsx")
    cluster_repository = ClusterRepository(ExcelAdapter(cluster_file))
    transaction_repository = TransactionRepository(ExcelAdapter(transaction_file))
    repository = ClusterAggregateRepository(cluster_repository, transaction_repository)
    clusters = repository.get_all_clusters()
    for cluster in clusters:
        print(cluster)
        [print(t) for t in cluster.transactions]


if __name__ == '__main__':
    main()
