_COVID_BASE = '/covid-19'

GLOBAL_DATA = '{}' + _COVID_BASE + '/all'

ALL_COUNTRIES = '{}' + _COVID_BASE + '/countries'
COUNTRY_DATA = ALL_COUNTRIES + '/{}'

ALL_STATES = '{}' + _COVID_BASE + '/states'
SINGLE_STATE = ALL_STATES + '/{}'

HISTORICAL_COUNTRY = '{}' + _COVID_BASE + '/historical/{}'
HISTORICAL_PROVINCE = HISTORICAL_COUNTRY + '/historical/{}'
STATE_COUNTY = '{}' + _COVID_BASE + '/historical/usacounties/{}'

ALL_CONTINENTS = '{}' + _COVID_BASE + '/continents'
CONTINENT_DATA = ALL_CONTINENTS + '/{}'

JHU_CSSE = '{}' + _COVID_BASE + '/jhucsse'
JHU_ALL_COUNTIES = JHU_CSSE + '/counties'
JHU_SINGLE_COUNTY = JHU_ALL_COUNTIES + '/{}'

NYT_USA = '{}' + _COVID_BASE + '/nyt/usa'
NYT_ALL_STATES = '{}' + _COVID_BASE + '/nyt/states'
NYT_SINGLE_STATE = '{}' + _COVID_BASE + '/nyt/states/{}'
NYT_ALL_COUNTIES = '{}' + _COVID_BASE + '/nyt/counties'
NYT_SINGLE_COUNTY = '{}' + _COVID_BASE + '/nyt/counties/{}'

APPLE_COUNTRIES = '{}' + _COVID_BASE + '/apple/countries'
APPLE_SUBREGIONS = APPLE_COUNTRIES + '/{}'
APPLE_SINGLE_SUBREGION = APPLE_SUBREGIONS + '/{}'

GOV_ALL = '{}' + _COVID_BASE + '/gov'
GOV_COUNTRY = GOV_ALL + '/{}'