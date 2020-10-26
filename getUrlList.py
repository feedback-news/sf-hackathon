from searchBing import search
import pandas as pd

def extractClaims():
    df = pd.read_csv('Covid_claims_cleaned.csv')
    claims = df["What fact-check ?"]
    return claims

def cleanClaims(claims):
    cleaned_claims = []
    for claim in claims:
        claim = claim.replace('\n', '')
        claim = claim.replace(',', '')
        claim = claim.replace('.', '')
        claim = claim.replace('\"', '')
        claim = claim.replace(' `` ', ' ')
        claim = claim.replace('things', '')
        claim = claim.replace('\"``', '')
        claim = claim.replace(' A ', ' ')
        claim = claim.replace('A ', ' ')
        claim = claim.replace('sent', '')
        claim = claim.replace('-', '')
        claim = claim.replace('In ', ' ')
        claim = claim.replace(' say ', ' ')
        claim = claim.replace(' says ', ' ')
        claim = claim.replace(' said ', ' ')
        claim = claim.replace( ' \'s', '\'s')
        claim = claim.replace(' used ', ' ')
        claim = claim.replace(' put ', ' ')
        claim = claim.replace('An ', '')
        claim = claim.replace('  ', ' ') # remove double spaces
        cleaned_claims.append(claim)
    return cleaned_claims

 
def populateCSV(claims):
    subscription_key = "ccbe9df154364869805417a8ac3d5adb"
 
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"

    missed_claim_claims = []
    missed_claim_numbers = []
    list_of_list_of_urls = []
    count = 0
    for claim in claims: 
        try:
            list_of_urls = search(search_url, claim, subscription_key, number_of_results=10)
        except:
            print("This did not work:" + str(claim))
            list_of_list_of_urls.append([])
            missed_claim_claims.append(claim)  
            missed_claim_numbers.append(count) 
        else:
            list_of_list_of_urls.append(list_of_urls)
        count += 1
        print(str(count))
    print(len(missed_claim_claims))

    df2 = pd.DataFrame(list_of_list_of_urls, index=list(claims))
    df2.to_csv('list-of-urls.csv')
    
    dfMissedClaims = pd.DataFrame(missed_claim_claims,index=missed_claim_numbers)
    dfMissedClaims.to_csv('missed_claims.csv')

def useUrlList():
    df = pd.read_csv('list-of-urls.csv')
    random = df.loc[1][2]
    print(random)

claims = extractClaims()
cleanClaims = cleanClaims(claims)
populateCSV(cleanClaims)
useUrlList()