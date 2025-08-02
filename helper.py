import numpy as np
def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()


    medal_tally["total"]=medal_tally["Gold"]+medal_tally["Silver"]+medal_tally["Bronze"]


    return medal_tally

def fetch_medal_tally(df,year,country):
    medal_df=df.drop_duplicates(subset=["Team","NOC","Games","Year","City","Sport","Event","Medal"])
    flag=0
    if year=="Overall" and country=="Overall":
        temp_df=medal_df
    if year=="Overall" and country!="Overall":
        flag=1
        temp_df=medal_df[medal_df["region"]==country]
    if year!="Overall" and country=="Overall":
        temp_df=medal_df[medal_df["Year"]==year]
    if year!="Overall" and country!="Overall":
        temp_df=medal_df[(medal_df["region"]==country) & (medal_df["Year"]==year)]


    if flag==1:
        x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

    x["total"]=x["Gold"]+x["Silver"]+x["Bronze"]
    return x



def country_year_list(df):
    years=df["Year"].unique().tolist()
    years.sort()
    years.insert(0,"Overall")
    country=np.unique(df["region"].dropna().values).tolist()  #NAN values must be removed , so dropna()
    country.sort() #sort alphabetically
    country.insert(0,"Overall") #sort alphabetically

    return years,country


def particapating_countries_over_time(df):
    nations_over_time = df.drop_duplicates(['Year','region'])['Year'].value_counts().reset_index().sort_values('Year')
    return nations_over_time

def events_over_time(df):
    number_of_ev=df.drop_duplicates(['Year','Event'])['Year'].value_counts().reset_index().sort_values('Year') 
    number_of_ev.columns = ['Year', 'Number of Events']
    return number_of_ev


def most_successful(df, sport):
    temp_df = df.dropna(subset=["Medal"])  # Keep only medal winners

    if sport != "Overall":
        temp_df = temp_df[temp_df["Sport"] == sport]  # Filter by sport

    top_athletes = temp_df['Name'].value_counts().reset_index().head(15)
    top_athletes.columns = ['Name', 'count']

    merged_df = top_athletes.merge(
        df[['Name', 'Sport', 'region']], on='Name', how='left'
    ).drop_duplicates('Name')

    merged_df = merged_df.reset_index(drop=True)

    return merged_df



def yearwise_medaltally(df,country):
    temp_df=df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=['Team',"NOC","Games","Year",'City','Sport','Event','Medal'],inplace=True) # same reasen like medal tally
    new_df=temp_df[temp_df["region"]==country]
    final_df=new_df.groupby("Year").count()["Medal"].reset_index()
    return final_df

def country_event_heatmap(df,country):
    temp_df=df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=['Team',"NOC","Games","Year",'City','Sport','Event','Medal'],inplace=True) # same reasen like medal tally
    new_df=temp_df[temp_df["region"]==country]
    pt=new_df.pivot_table(index="Sport",columns="Year",values="Medal",aggfunc='count').fillna(0)
    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=["Medal"])  # Keep only medal winners

    
    temp_df = temp_df[temp_df["region"] == country]  # Filter by Country

    top_athletes = temp_df['Name'].value_counts().reset_index().head(15)
    top_athletes.columns = ['Name', 'count']

    merged_df = top_athletes.merge(
        df[['Name', 'Sport']], on='Name', how='left'
    ).drop_duplicates('Name')

    merged_df = merged_df.reset_index(drop=True)

    return merged_df


def weight_v_height(df,sport):
    athlete_df=df.drop_duplicates(subset=["Name","region"])
    athlete_df["Medal"].fillna("No Medal",inplace=True)
    if sport!="Overall":
        temp_df=athlete_df[athlete_df["Sport"]==sport]
        return temp_df
    else:
        return athlete_df


def men_v_women(df):
    athlete_df=df.drop_duplicates(subset=["Name","region"])
    men=athlete_df[athlete_df["Sex"]=="M"].groupby("Year").count()["Name"].reset_index()
    women=athlete_df[athlete_df["Sex"]=="F"].groupby("Year").count()["Name"].reset_index()
    final=men.merge(women,on="Year")
    final.rename(columns={"Name_x":"Male","Name_y":"Female"},inplace=True)
    final.fillna(0,inplace=True)
    return final