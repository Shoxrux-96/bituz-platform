from idanalyzer import CoreAPI
from decouple import config


ID_VERUFICATION_API_KEY = config("ID_VERIFICATION_API")


coreapi = CoreAPI(ID_VERUFICATION_API_KEY)


response = coreapi.scan(document_primary='path_to_id.jpg')

# Print extracted results
print(response)
