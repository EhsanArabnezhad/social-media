import json
import watson_developer_cloud as WDC
from watson_developer_cloud.natural_language_understanding_v1 import Features, KeywordsOptions, EntitiesOptions, CategoriesOptions, EmotionOptions, SentimentOptions
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('ShRN-7WQV3_D6nwRyJwTJjU1nDtaDapjo6CYs8-cQhEU')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2019-07-12',
    authenticator=authenticator
)


text="Ecco nel dettaglio i nuovi importi e limiti di reddito per assegni e pensioni di invalidita civile"


natural_language_understanding.set_service_url('https://gateway-lon.watsonplatform.net/natural-language-understanding/api')

response = natural_language_understanding.analyze(
    text=text,
    features=Features(
        sentiment=SentimentOptions())).get_result()

print(json.dumps(response, indent=2))