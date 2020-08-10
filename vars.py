from collections import OrderedDict
import numpy as np

DB_NAME = 'college_scorecard'

# SQL to create tables
TABLES = OrderedDict()

TABLES['states'] = (
    "CREATE TABLE IF NOT EXISTS `states` ("
    "  `state_id` INT NOT NULL, "
    "  `long_state` VARCHAR(50), "
    "  `abbr_state` CHAR(2) NOT NULL, "
    "  `region` VARCHAR(50), "
    "  CONSTRAINT pk PRIMARY KEY (`state_id`)"
    ") ENGINE=InnoDB")

TABLES['controls'] = (
    "CREATE TABLE IF NOT EXISTS `controls` ("
    "  `control_id` INT NOT NULL, "
    "  `control` VARCHAR(20) NOT NULL, "
    "  CONSTRAINT pk PRIMARY KEY (`control_id`)"
    ") ENGINE=InnoDB")

TABLES['levels'] = (
    "CREATE TABLE IF NOT EXISTS `levels` ("
    "  `level_id` INT NOT NULL, "
    "  `level` VARCHAR(20) NOT NULL, "
    "  CONSTRAINT pk PRIMARY KEY (`level_id`)"
    ") ENGINE=InnoDB")

TABLES['institutions'] = (
    "CREATE TABLE IF NOT EXISTS `institutions` ("
    "  `inst_id` INT NOT NULL AUTO_INCREMENT, "
    "  `name` VARCHAR(255) NOT NULL, "
    "  `city` VARCHAR(50), "
    "  `state_id` INT, "
    "  `control_id` INT, "
    "  `level_id` INT, "
    "  `mean_earn` INT, "
    "  `family_inc` FLOAT(10,2), "
    "  `mean_cost` INT, "
    "  `first_gen` FLOAT(10,2), "
    "  CONSTRAINT pk PRIMARY KEY (`inst_id`), "
    "  CONSTRAINT state FOREIGN KEY (`state_id`) REFERENCES `states`(`state_id`) ON DELETE SET NULL, "
    "  CONSTRAINT control FOREIGN KEY (`control_id`) REFERENCES `controls`(`control_id`) ON DELETE SET NULL, "
    "  CONSTRAINT level FOREIGN KEY (`level_id`) REFERENCES `levels`(`level_id`) ON DELETE SET NULL"
    ") ENGINE=InnoDB")

# ********************************************************************************

# Columns to load from dataset
COLS = ['UNITID', 'INSTNM', 'CITY', 'STABBR', 'ST_FIPS', 'REGION', 'CONTROL', 'ICLEVEL',
        'MN_EARN_WNE_P10', 'FAMINC', 'NPT4_PUB', 'NPT4_PRIV', 'FIRST_GEN']

DTYPES = {
    'UNITID': np.int64,
    'INSTNM': str,
    'CITY': str,
    'STABBR': str,
    'ST_FIPS': np.int64,
    'REGION': np.int64,
    'CONTROL': np.int64,
    'ICLEVEL': np.int64,
    'MN_EARN_WNE_P10': np.float64,
    'FAMINC': np.float64,
    'NPT4_PUB': np.float64,
    'NPT4_PRIV': np.float64,
    'FIRST_GEN': np.float64
}