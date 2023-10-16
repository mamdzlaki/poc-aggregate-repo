import pytest
from domain.repository import ClusterAggregateRepository, ClusterRepository, TransactionRepository
from domain.adapter import ExcelAdapter
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def cluster_repository():
    cluster_file = os.path.join(ROOT_DIR, "data/clusters.xlsx")
    return ClusterRepository(ExcelAdapter(cluster_file))


@pytest.fixture
def transaction_repository():
    transaction_file = os.path.join(ROOT_DIR, "data/transactions.xlsx")
    return TransactionRepository(ExcelAdapter(transaction_file))


def test_get_all_clusters(cluster_repository, transaction_repository):
    cluster_root_repository = ClusterAggregateRepository(cluster_repository, transaction_repository)
    clusters = cluster_root_repository.get_all_clusters()
    assert len(clusters) == 14
