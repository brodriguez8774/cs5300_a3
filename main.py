"""
Recurrent Neural Net.
"""

# System Imports.
import keras

# User Class Imports.
from resources import logging
import neural_net


# Initialize logging.
logger = logging.get_logger(__name__)


recurrent_net = neural_net.RecurrentNet(data_source='trump')
# recurrent_net.import_weights('Documents/Weights/2LSTMS_Size215_atEpoch0')
recurrent_net.train(num_epochs=100000)
recurrent_net = None

