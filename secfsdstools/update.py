""" Getting everything ready to work with the data. """
from secfsdstools._0_config.configmgt import ConfigurationManager, Configuration
from secfsdstools._1_setup.setupdb import DbCreator
from secfsdstools._2_download.secdownloading import SecZipDownloader, UrlDownloader


def update(config_file: str = None):
    """
    ensures that all available zip files are downloaded and that the index is created.
    """

    # read config
    config: Configuration = ConfigurationManager(filename=config_file).get_configuration()

    # create the db
    DbCreator(db_dir=config.db_dir).create_db()

    # download actual data
    url_downloader = UrlDownloader(user_agent=config.user_agent_email)
    SecZipDownloader(zip_dir=config.download_dir, urldownloader=url_downloader).download()

    # create index of reports


if __name__ == '__main__':
    import logging

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    update("../secsdfstools.cfg")