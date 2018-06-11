"""
Neural Net logic.
"""

# System Imports.
import json, keras

# User Class Imports.
from resources import logging


# Initialize logging.
logger = logging.get_logger(__name__)


class RecurrentNet():
    """
    Recurrent Neural Net using the Keras library.
    """
    def __init__(self):
        logger.info('Starting Recurrent Net.')
        self.data = self.import_data()

    def __del__(self):
        logger.info('Recurrent Net finished.')

    def import_data(self):
        """
        Read through and import contents of tweets.

        Twitter was chosen due to all data having limited message length.
        Trump Tweets were chosen due to being generally one of the most documented and well archived accounts.
        :return: Array of tweet messages.
        """
        try:
            pass
            file = open('Documents/trump_tweets_2017.json', 'r')

            dataset_import = json.load(file)
            dataset = []
            for line in dataset_import:
                dataset.append(line['text'])

            file.close()
            logger.info(dataset)
            return dataset

        except Exception:
            logger.error('Error reading file.')
            logger.error(Exception, exc_info=True)


