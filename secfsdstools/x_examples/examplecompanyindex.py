"""
Examples for CompanyReader
"""
from typing import Dict, List

from secfsdstools.c_index.companyindexreading import CompanyIndexReader
from secfsdstools.c_index.indexdataaccess import IndexReport


def run():
    # pylint: disable=W0612
    """
    run the example
    """
    apple_cik: int = 320193

    # getting the company index reader instance for apple
    apple_idx_reader = CompanyIndexReader.get_company_index_reader(apple_cik)

    # get the information of the latest filing
    latest_filing: Dict[str, str] = apple_idx_reader.get_latest_company_filing()
    print(latest_filing)

    # get basic infos of all the reports the company has filed.
    # ... first as a pandas DataFrame
    apple_all_reports_df = apple_idx_reader.get_all_company_reports_df()

    # ... second as list of IndexReport instances
    apple_all_reports: List[IndexReport] = apple_idx_reader.get_all_company_reports()
    print("first entry: ", apple_all_reports[0])

    # both method can also be used with filters for the form, the report type.
    # for instance, if you are only interested in annual and quarter reports, you can use
    apple_10k_and_10q_reports_df = apple_idx_reader.get_all_company_reports_df(
        forms=['10-K', '10-Q'])

    print(apple_10k_and_10q_reports_df)


if __name__ == '__main__':
    run()
