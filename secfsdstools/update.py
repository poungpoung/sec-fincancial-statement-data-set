""" Getting everything ready to work with the data. """
import logging

from secfsdstools.a_config.configmgt import ConfigurationManager, Configuration
from secfsdstools.b_setup.setupdb import DbCreator
from secfsdstools.c_download.secdownloading import SecZipDownloader
from secfsdstools.c_download.rapiddownloading import RapidZipDownloader
from secfsdstools.d_index.indexing import ReportZipIndexer

LOGGER = logging.getLogger(__name__)


def update(config: Configuration = None):
    """
    ensures that all available zip files are downloaded and that the index is created.
    """

    # read config
    if config is None:
        LOGGER.info("reading configuration file ..")
        config = ConfigurationManager.read_config_file()

    # create the db
    DbCreator(db_dir=config.db_dir).create_db()

    # download data from sec.gov
    LOGGER.info("start to download files from sec.gov ...")
    secdownloader = SecZipDownloader.get_downloader(configuration=config)
    secdownloader.download()

    # download data from rapid
    # todo: check if rapid is set
    LOGGER.info("start to download files from rapid...")
    rapiddownloader = RapidZipDownloader.get_downloader(configuration=config)
    try:
        rapiddownloader.download()
    except Exception as ex:
        LOGGER.warning("Failed to get data from rapid api, please check rapid-api-key. " +
                       "Only using data from Sec.gov: %s", ex)

    # create index of reports
    LOGGER.info("start to index downloaded files ...")
    indexer = ReportZipIndexer(db_dir=config.db_dir, zip_dir=config.download_dir)
    indexer.process()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(module)s  %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    update()
        # Configuration(
        #     db_dir='c:/ieu/projects/sec-fincancial-statement-data-set/data/db/',
        #     download_dir='c:/ieu/projects/sec-fincancial-statement-data-set/data/dld/',
        #     user_agent_email='your.email@goes.here'
        # ))
