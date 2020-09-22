import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from io import BytesIO
import base64

def load_data():
    # Read data
    insurance = pd.read_csv('data/autoinsurance.csv')
    
    # Adjust dtypes
    catcol = insurance.select_dtypes('object').columns
    insurance[catcol] = insurance[catcol].apply(lambda x: x.astype('category'))
    
    return(insurance)


def plot_age(data):
    
    # ---- Age group of customer

    def age_grouping(data):
        if(data.age <= 24):
            return '19 - 24'
        elif(data.age > 24 and data.age <= 30) : 
            return '25 - 30'
        elif(data.age > 30 and data.age <= 35) : 
            return '31 - 35'
        elif(data.age > 35 and data.age <= 40) : 
            return '36 - 40'
        elif(data.age > 40 and data.age <= 45) : 
            return '41 - 45'
        elif(data.age > 45 and data.age <= 50) : 
            return '46 - 50'
        elif(data.age > 50 and data.age <= 55) : 
            return '51 - 55'
        elif(data.age > 55 and data.age <= 59) : 
            return '56 - 59'
        else : 
            return '60+'
        

    data['age_group'] = data.apply(age_grouping,axis = 1)

    fraud_data = data[data['fraud_reported'] == 'Y']
    age_profile = pd.crosstab(index = fraud_data['age_group'], columns = 'Jumlah')
    
    ax = age_profile.plot.barh(title = "Fraud Reported by Age group", 
    legend= False, 
    color = '#c34454', 
    figsize = (8,6))
    
    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png', transparent=True)
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_premium(data):

    def tocolor(data):
        if(data.fraud_reported == 'Y'):
            return '#53a4b1'
        else : 
            return '#c34454'
    
    data.fcolor = data.apply(tocolor,axis=1)
    
    # ---- Months as Customer per Policy Annual Premium

    
    ax = data.plot.scatter(x= 'months_as_customer', 
                       y = 'policy_annual_premium', 
                       c=data.fcolor,title = "Months as Customer per Policy Annual Premium",
                       figsize=(8, 6))

    # Plot Configuration
    lab_y = mpatches.Patch(color='#53a4b1', label='Y')
    lab_n = mpatches.Patch(color='#c34454', label='N')
    plt.legend(handles = [lab_y ,lab_n])
    plt.xlabel("Months as Customer")
    plt.ylabel("Policy Annual Premium")

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)



def plot_incident(data):

    def tonum(data):
        if(data.fraud_reported == 'Y'):
            return 1
        else : 
            return 0
    
    data['fnum'] = data.apply(tonum,axis=1)

    
    timeseries = data.pivot_table(
                index='incident_date',
                values='fraud_reported',
                aggfunc='count').ffill()
    
    # ---- Number of Report per Day

    ax = timeseries.plot(legend=False, title = "Number of Fraud per Day",color='#c34454', figsize=(8, 6))

    # Plot Configuration
    plt.xlabel('')

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_report(data):
    
    df_fraud = data[data.fraud_reported == 'Y'].pivot_table(index='police_report_available',values='fraud_reported',aggfunc='count')

    df_nfraud = data[data.fraud_reported == 'N'].pivot_table(index='police_report_available',values='fraud_reported',aggfunc='count')

    
    # ---- Police Report Availability

    ax = pd.concat([df_fraud,df_nfraud],axis=1).plot.bar(stacked = True,color =['#c34454','#53a4b1'],title = "Police Report Availability", figsize=(8, 6))
    
    # Plot Configuration
    plt.legend(['fraud','not fraud'], bbox_to_anchor=(1, 1))
    plt.xlabel("police report available'")

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_amount_claim(data):
        
    df_injury_claim = data[data.fraud_reported == 'Y'].pivot_table(index='auto_year',values='injury_claim',aggfunc='sum')
    df_property_claim = data[data.fraud_reported == 'Y'].pivot_table(index='auto_year',values='property_claim',aggfunc='sum')
    df_vehicle_claim = data[data.fraud_reported == 'Y'].pivot_table(index='auto_year',values='vehicle_claim',aggfunc='sum')
    claim_report = pd.concat([df_injury_claim,df_property_claim,df_vehicle_claim],axis=1)
    ax = claim_report.plot.bar(stacked = True,color =['#c34454','#53a4b1','#00FF00'],title = "Amount Claim", figsize=(8, 6))
    
    # Plot Configuration
    plt.legend(['Injury','Property','Vehicle'], bbox_to_anchor=(1, 1))
    plt.xlabel("Auto Year")

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_total_claim(data):
        
    df_fraud = data[data.fraud_reported == 'Y'].pivot_table(index='auto_year',values='fraud_reported',aggfunc='count')
    df_nfraud = data[data.fraud_reported == 'N'].pivot_table(index='auto_year',values='fraud_reported',aggfunc='count')

    claim_report = pd.concat([df_fraud,df_nfraud],axis=1)

    ax = claim_report.plot.barh(stacked = False,color =['#FF9900','#0000FF'],title = "Total Claim", figsize=(8, 6))

    # Plot Configuration
    plt.legend(['Fraud','No Fraud'], bbox_to_anchor=(1, 1))
    plt.xlabel("Auto Year")

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_incident_city(data):
          
    claim_report = data[data.fraud_reported == 'Y'].pivot_table(index='incident_city',values='fraud_reported',aggfunc='count')
    ax = claim_report.sort_values(by='fraud_reported', ascending=False).plot.bar(color =['#c34454','#53a4b1'],title = "Incident City", figsize=(8, 6),sort_columns=True)

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)

def plot_incident_hour(data):
          
    df_fraud = data[data.fraud_reported == 'Y'].pivot_table(index='incident_hour_of_the_day',values='fraud_reported',aggfunc='count')
    df_nfraud = data[data.fraud_reported == 'N'].pivot_table(index='incident_hour_of_the_day',values='fraud_reported',aggfunc='count')

    claim_report = pd.concat([df_fraud,df_nfraud],axis=1)

    ax = claim_report.plot.bar(color =['#c34454','#53a4b1'],title = "Incident Hour Of The Day", figsize=(8, 6))

    # Plot Configuration
    plt.legend(['Fraud','No Fraud'], bbox_to_anchor=(1, 1))
    plt.xlabel("Incident Hour Of The Day")

    # Save png file to IO buffer
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]

    return(result)