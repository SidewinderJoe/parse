import pandas as pd
import probablepeople

filename = input('Please enter list name: ')

df = pd.read_csv(filename)
names = df.Name

def remove_whitespace(x):
    """
    Helper function to remove any blank space from a string
    x: a string
    """
    try:
        # Remove spaces inside of the string
        x = " ".join(x.split())

    except:
        pass
    return x


i = 0
print("Processing {} records...".format(names.count()))
for n in names:
    try:
        pp = probablepeople.tag(n)[0]
        if 'GivenName' not in pp and 'Surname' in pp:
            df.at[i, 'Salutation'] = '{}'.format(pp.get('Surname', ''))
        if 'GivenName' in pp:
            df.at[i, 'Salutation'] = '{}'.format(pp.get('GivenName', ''))
        if 'GivenName' in pp and 'And' in pp:
            df.at[i, 'Salutation'] = '{}'.format(pp.get('GivenName', ''))
        if 'GivenName' in pp and 'And' in pp and 'SecondGivenName' in pp:
            df.at[i, 'Salutation'] = '{} {} {}'.format(pp.get('GivenName', ''), pp.get('And', ''), pp.get('SecondGivenName', ''))
        if 'CorporationName' in pp or 'CorporationNameOrganization' in pp or 'CorporationNameBranchType' in pp or 'CorporationNameBranchIdentifier' in pp or 'CorporationLegalType' in pp:
            df.at[i, 'Salutation'] = '{} {} {} {} {}'.format(pp.get('CorporationName', ''), pp.get('CorporationNameOrganization', ''), pp.get('CorporationNameBranchType', ''), pp.get('CorporationNameBranchIdentifier', ''), pp.get('CorporationLegalType', ''))
    except:
        df.at[i, 'Skip'] = 'X'
    finally:
        i+=1

df.Salutation = df.Salutation.apply(remove_whitespace)
df.to_csv('test.csv', encoding='utf-8')

print("Complete")