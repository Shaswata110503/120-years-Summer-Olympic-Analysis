import pandas as pd
import streamlit as st
import preprocessor,helper
import plotly.io as pio
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import scipy.stats

'''Streamlit is an open-source Python library for building interactive web apps using only Python. It's ideal for creating dashboards, data-driven web apps, reporting tools and interactive user interfaces without needing HTML, CSS or JavaScript.'''

st.set_page_config(page_title="Olympics Dashboard", layout="wide", initial_sidebar_state="collapsed")


df=pd.read_csv(r'C:\Users\desha\OneDrive\Desktop\MYCODE\Data Analysis\athlete_events.csv')
region_df=pd.read_csv(r'C:\Users\desha\OneDrive\Desktop\MYCODE\Data Analysis\noc_regions.csv')

df=preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image(r"C:\Users\desha\OneDrive\Desktop\MYCODE\Data Analysis\Olympic_rings_without_rims.png")

user_menu=st.sidebar.radio(
    'Select an Option',
    ('Home','Medal Tally','Overall  Analysis',"Country-wise analysis","Athlete wise Analysis")
)

if user_menu == "Home":
    st.markdown("<h1 style='text-align: center; color: darkblue;'>🏅 Olympic Data Analyzer</h1>", unsafe_allow_html=True)    
    st.markdown("""
    ## 📊 Project Overview
    This interactive dashboard explores **120+ years of Olympic history** using athlete and medal data.
    
    **Features include:**
    - 🥇 Medal Tally analysis by year and country
    - 🌍 Country-wise performance heatmaps
    - 👤 Athlete-level stats: age, gender, weight, height
    - 📈 Trends over time (events, nations, gender participation)
    
    ---
    ## 🧰 Dataset Used
    - `athlete_events.csv` (from Kaggle)
    - `noc_regions.csv` for country mapping

    ---
    ## 👨‍💻 How to Use
    - Use the sidebar to navigate between sections.
    - Select years/countries/sports as filters.
    - View interactive plots and tables dynamically.
    
    ---
    > Built with ❤️ using Streamlit, pandas, seaborn, plotly.
    """, unsafe_allow_html=True)




if(user_menu=='Medal Tally'):
    st.sidebar.header("Medal Tally")
    years,country=helper.country_year_list(df)
    selected_year=st.sidebar.selectbox("Select Year",years)

    selected_country=st.sidebar.selectbox("Select Country",country)

    medal_tally=helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year=="Overall" and selected_country=="Overall":
        st.title("Overall Tally")

    if selected_year=="Overall" and selected_country!="Overall":
        st.title(f"Overall Tally of {selected_country}")

    if selected_year!="Overall" and selected_country=="Overall":
        st.title(f"Overall Tally of {selected_year}")

    if selected_year!="Overall" and selected_country!="Overall":
        st.title(f"Tally of {selected_country} in the year {selected_year}")


    st.table(medal_tally)



    st.title("🏅 Yearwise Medal Tally Comparison")
    countries = sorted(df['region'].dropna().unique())
    country1=st.selectbox("Select Country",countries)
    country2=st.selectbox("Select another Country",countries)
    final_df =helper.yearwise_medaltally_comparison(df, country1,country2)

    # Plotting the comparison
    fig = px.line(final_df,
                      x='Year',
                      y=[country1, country2],
                      labels={"value": "Medal Count", "variable": "Country"},
                      title=f"Year-wise Medal Tally: {country1} vs {country2}")
    st.plotly_chart(fig, use_container_width=True)




if(user_menu=='Overall  Analysis'):
    cities=df['City'].unique().shape[0]
    editions=df['Year'].unique().shape[0]-1
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]

    st.title("Top Statistics")

    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)



    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time=helper.particapating_countries_over_time(df)
    

    fig = px.line(nations_over_time,
              x='Year',
              y='count',
              markers=True,
              labels={'count': 'Number of Countries'})

    # Customize line and marker colors
    fig.update_traces(line=dict(color='green'),
                    marker=dict(color='red', size=8))
    
    st.title("Participating Nations over the years")

    st.plotly_chart(fig, use_container_width=True)



    events_over_time=helper.events_over_time(df)
    

    fig = px.line(events_over_time,
              x='Year',
              y='Number of Events',
              markers=True,
              labels={'count': 'Number of Events'})

    # Customize line and marker colors
    fig.update_traces(line=dict(color='green'),
                    marker=dict(color='red', size=8))
    
    st.title("Number of Events over the years")

    st.plotly_chart(fig, use_container_width=True)


    st.title("No. of events over the time(Every Sport)")
    fig,ax=plt.subplots(figsize=(15,15))
    x=df.drop_duplicates(["Year","Sport","Event"])  #same year, same sports and same events are removed so that we get genunine number of sport anf events
    ax=sns.heatmap(x.pivot_table(index="Sport",columns='Year',values="Event",aggfunc="count").fillna(0).astype("int"),annot=True)

    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list=df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,"Overall")

    selected_sport=st.selectbox("Select a sport",sport_list)
    x=helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu=="Country-wise analysis":

    st.sidebar.title("Country wise Analysis")
    country_list=df["region"].dropna().unique().tolist()
    country_list.sort()
    selected_country=st.sidebar.selectbox("Select Country",country_list)

    country_df=helper.yearwise_medaltally(df,selected_country)
    fig = px.line(country_df,
              x='Year',
              y='Medal',
            #   markers=True,
              )

    # # Customize line and marker colors
    # fig.update_traces(line=dict(color='green'),
    #                 marker=dict(color='red', size=8))
    
    st.title(f"Yearwise Medal tally of {selected_country}")
    st.plotly_chart(fig, use_container_width=True)
        

    st.title(f"Excels of {selected_country} in Different sports")
    pt=helper.country_event_heatmap(df,selected_country)
    if pt.empty:
        st.warning(f"No medal data found for {selected_country}.")
    else:
        fig,ax=plt.subplots(figsize=(15,15))
        ax=sns.heatmap(pt,annot=True)
        st.pyplot(fig)

    st.title(f"Top 15 Athletes of {selected_country}")
    top10_df=helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)




if user_menu=="Athlete wise Analysis":
    athlete_df=df.drop_duplicates(subset=["Name","region"])
    x1=athlete_df["Age"].dropna()
    x2=athlete_df[athlete_df["Medal"]=="Gold"]["Age"].dropna()
    x3=athlete_df[athlete_df["Medal"]=="Silver"]["Age"].dropna()
    x4=athlete_df[athlete_df["Medal"]=="Bronze"]["Age"].dropna()
    

    fig = ff.create_distplot(
    [x1,x2,x3,x4],   
    ["Overall Age","Gold Medalist","Silver Medalist","Bronze Medalist"],           
    show_hist=False,
    show_rug=False
    )   

    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)


    x = []
    name = []

    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
        'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
        'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
        'Water Polo', 'Hockey', 'Rowing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
        'Tennis','Golf', 'Softball', 'Archery',
        'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
        'Rhythmic Gymnastics', 'Rugby Sevens',
        'Beach Volleyball', 'Triathlon', 'Rugby','Polo',
        'Ice Hockey']

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df["Sport"] == sport]
        x.append(temp_df[temp_df["Medal"] == "Gold"]["Age"].dropna())
        name.append(sport)


    # Create distplot
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)

    # Streamlit output
    st.title("Distribution of Age with respect to Sports (Gold Medalists)")
    st.plotly_chart(fig)


    xs=[]
    names=[]

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df["Sport"] == sport]
        xs.append(temp_df[temp_df["Medal"] == "Silver"]["Age"].dropna())
        names.append(sport)


    # Create distplot
    fig = ff.create_distplot(xs, names, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)

    # Streamlit output
    st.title("Distribution of Age with respect to Sports (Silver Medalists)")
    st.plotly_chart(fig)
    
    
    
    




    # Initialize data holders
    xb = []
    nameb = []

    # Loop through the sports and filter valid Bronze medalist age data
    for sport in famous_sports:
        temp_df = athlete_df[
            (athlete_df["Sport"] == sport) &
            (athlete_df["Medal"] == "Bronze")
        ]["Age"].dropna()

        # Check if KDE can be computed
        if len(temp_df) >= 2 and temp_df.nunique() > 1:
            try:
                _ = scipy.stats.gaussian_kde(temp_df)  # test KDE
                xb.append(temp_df)
                nameb.append(sport)
            except Exception as e:
                print(f"⚠️ Skipped {sport} due to KDE error: {e}")
        else:
            print(f"⛔ Skipped {sport}: insufficient unique Bronze age data.")

    # Plotting
    if len(xb) > 0 and len(xb) == len(nameb):
        fig = ff.create_distplot(xb, nameb, show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=1000, height=600)
        st.title("Distribution of Age with respect to Sports (Bronze Medalists)")
        st.plotly_chart(fig)
    else:
        st.warning("No valid Bronze medalist age distributions available to plot.")




    sport_list=df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,"Overall")
    st.title("Heigh vs Weight")
    selected_sport=st.selectbox("Select a sport",sport_list)
    temp_df=helper.weight_v_height(df,selected_sport)
    fig,ax=plt.subplots()
    ax=sns.scatterplot(x=temp_df["Weight"],y=temp_df["Height"],hue=temp_df["Medal"],style=temp_df["Sex"],s=60)
    
    st.pyplot(fig)


 
    st.title("Men Vs Women Participation Over the time")
    final=helper.men_v_women(df)
    fig=px.line(final,x="Year",y=["Male","Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)