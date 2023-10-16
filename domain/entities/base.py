from dataclasses import dataclass
from datetime import date
from typing import Optional
from typing import TypedDict


@dataclass
class Cluster:
    id: str
    name: str
    start_date: date
    end_date: date
    prop_1: Optional[str] = None
    prop_2: Optional[str] = None
    transactions: list["Transaction"] = None

    @classmethod
    def from_dto(cls, dto: "ClusterDTO"):
        return cls(
            id=dto.cluster_id,
            name=dto.cluster_name,
            start_date=dto.start_date,
            end_date=dto.end_date,
            prop_1=dto.prop_1,
            prop_2=dto.prop_2
        )


@dataclass
class ClusterDTO:
    cluster_id: str
    cluster_name: str
    start_date: date
    end_date: date
    prop_1: str
    prop_2: str

    @classmethod
    def from_dict(cls, row: dict) -> "ClusterDTO":
        return cls(
            cluster_id=row["Cluster Id"],
            cluster_name=row["Cluster Name"],
            start_date=row["Start Date"],
            end_date=row["End Date"],
            prop_1=row["Prop1"],
            prop_2=row["Prop2"]
        )



@dataclass
class Transaction:
    id: str
    transaction_date: date
    volume: float
    quantity: int

    @classmethod
    def from_dto(cls, dto: "TransactionDTO"):
        return cls(
            id=dto.transaction_id,
            transaction_date=dto.transaction_date,
            volume=float(dto.volume),
            quantity=int(dto.quantity),
        )


@dataclass
class TransactionDTO:
    transaction_id: str
    cluster_id: str
    transaction_date: date
    volume: str
    quantity: str

    @classmethod
    def from_dict(cls, row:  dict) -> "TransactionDTO":
        return cls(
            transaction_id=row["Transaction Id"],
            cluster_id=row["Cluster Id"],
            transaction_date=row["Transaction Date"],
            volume=row["Volume"],
            quantity=row["Quantity"]
        )
