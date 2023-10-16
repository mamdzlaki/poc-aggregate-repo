from abc import ABC, abstractmethod

import pandas as pd


class DataframeAdapter(ABC):
    @abstractmethod
    def load_dataframe(self) -> pd.DataFrame:
        pass


class ExcelAdapter(DataframeAdapter):
    """ Adapter for reading Excel files to Dataframe"""
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def load_dataframe(self) -> pd.DataFrame:
        """ Load Excel file to Dataframe
        Returns:
            pd.DataFrame: Excel file loaded to Dataframe
        """
        return pd.read_excel(self.filepath)
