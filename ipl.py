import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns
import cricstats

batsman_bowler = st.sidebar.radio("Batsman or Bowler Analysis",
                 ('Batsman',
                 "Bowler"))
ipl_season = st.sidebar.selectbox("IPL Season",
("2007","2009",
"2010",
"2011",
"2012",
"2013",
"2014",
"2015",
"2016",
"2017",
"2018",
"2019",
"2020","2021","All Seasons"))

if batsman_bowler == "Batsman":
    strategy = st.sidebar.selectbox("Select Analysis Strategy",
                    ('Batsman Ranking ( 6 dimensions )',
                    'Runs',
                    'Most Fours',
                    'Most Sixes',
                    'Highest Average',
                    'Highest Strike Rate',
                    'Most Centuries',
                    'Most Fifties',
                    'Most Thirties',
                    "CHT"))
else:
    strategy = st.sidebar.selectbox("Select Analysis Strategy",
                    ('Bowler Ranking ( 4 dimensions )',
                    'Most Wickets',
                    'Best Average',
                    'Best Strike Rate',
                    'Best Economy',
                    'Bowler Ranking ( 4 dimensions )'))

title_page_header = "# IPL " + str(ipl_season) + " Analysis"
st.markdown(title_page_header)     

import matplotlib.pyplot as plt
import seaborn as sns

def draw_plot(fig_size_x = 10,
              fig_size_y =  10,
              tick_params_labelsize = 14,
             xlabel_name_fontsize = 20,
             ylabel_name_fontsize = 20,
             title_name_fontsize = 20,
             xlabel_name = "",
             ylabel_name = "",
             title_name = ""):
    
    #get current figure 
    fig=plt.gcf()
    
    #set the size of the figure
    fig.set_size_inches(fig_size_x,fig_size_y)

    #get axes of the current figure 
    ax =  fig.gca()

    # set the label size of the ticks of the axes
    ax.tick_params(labelsize=tick_params_labelsize)

    # set the label size of the x axis
    ax.set_xlabel(xlabel_name,fontsize = xlabel_name_fontsize)

    # set the label size of the y axis
    ax.set_ylabel(ylabel_name,fontsize = ylabel_name_fontsize)

     # set the title of the plot
    ax.set_title(title_name,fontsize = title_name_fontsize)


def display_category(filename,ipl_season= ""):
    batsman_stats = cricstats.get_batsman_stats(filename,ipl_season)

    if strategy == "Runs":
        display_batsman_runs(batsman_stats)
    elif strategy == "Most Fours":
        display_fours_six(batsman_stats,4,"batsman_fours")
    elif strategy == "Most Sixes":
        display_fours_six(batsman_stats,6,"batsman_six")
    elif strategy == "Highest Average":
        display_batsman_average(batsman_stats)
    elif strategy == "Highest Strike Rate":
        display_batsman_strike_rate(batsman_stats)
    elif strategy == "Most Centuries":
        display_batsman_milestone(batsman_stats,"century")
    elif strategy == "Most Fifties":
        display_batsman_milestone(batsman_stats,"fifty")
    elif strategy == "Most Thirties":
        display_batsman_milestone(batsman_stats,"thirty")
    elif strategy == "CHT":
        display_CHT(batsman_stats)
    elif strategy == "Batsman Ranking ( 6 dimensions )":
        display_batsman_ranking(batsman_stats)


def get_bowler_average(bowler_stats):
    bowler_stats = bowler_stats.sort_values(by = "average",ascending = True)
    xlabel_name = "Average"
    ylabel_name = "Bowler"
    title_name = " Bowler Average Distribution [ Runs / Wickets ]"

    sns.barplot( x = "average" , y = "bowler" , data = bowler_stats.head(10), color = "blue")

    draw_plot(xlabel_name = xlabel_name ,
                ylabel_name = ylabel_name,
                title_name = title_name)

    fig = plt.gcf()
    ax = fig.gca()

    for i , v in enumerate(bowler_stats.head(10)["average"].values):
        ax.text(2, i, v,fontsize=16,color='white',weight='bold')

    st.pyplot(fig)

def display_batsman_runs(batsman_runs):

        xlabel_name = "Runs"
        ylabel_name = "Batsman"
        title_name = " Batsman Runs Distribution"

        sns.barplot( x = "batsman_runs" , y = "batsman" , data = batsman_runs.head(10), color = "blue")

        draw_plot(xlabel_name = xlabel_name ,
                    ylabel_name = ylabel_name,
                    title_name = title_name)

        fig = plt.gcf()
        ax = fig.gca()


        for i , v in enumerate(batsman_runs.head(10)["batsman_runs"].values):
            ax.text(300, i, v,fontsize=16,color='white',weight='bold')

        st.pyplot(fig)

def get_boundary(all_data,boundary,boundary_name):
    
    all_data_boundary = all_data[(all_data["runs_batsman"] == boundary)]
    boundary_runs = all_data_boundary.groupby(["batsman"])["batsman"].count() \
.reset_index( name = boundary_name).sort_values( by = boundary_name,ascending = False) 
   
    return(boundary_runs)
    

def display_fours_six(boundary_runs,boundary,boundary_name):
        boundary_runs = boundary_runs.sort_values(by =boundary_name,ascending =False)

        xlabel_name = str(boundary) + " runs "
        ylabel_name = "Batsman"
        title_name = " Batsman " + str(boundary) + " Distribution "

        sns.barplot( x = boundary_name , y = "batsman" , data = boundary_runs.head(10), color = "purple")

        draw_plot(xlabel_name = xlabel_name ,
                    ylabel_name = ylabel_name,
                    title_name = title_name)

        fig = plt.gcf()
        ax = fig.gca()


        for i , v in enumerate(boundary_runs.head(10)[boundary_name].values):
            ax.text(5, i, v,fontsize=16,color='white',weight='bold')
        
        st.pyplot(fig)

def display_batsman_average(batsman_all_stats):
    batsman_all_stats = batsman_all_stats[batsman_all_stats["batsman_runs"] >= 300]
    batsman_all_stats = batsman_all_stats.sort_values(by ="average",ascending =False)
    xlabel_name = "average"
    ylabel_name = "Batsman"
    title_name = " Batsman average Distribution"

    sns.barplot( x = "average" , y = "batsman" , 
    data = batsman_all_stats.head(10), color = "red")

    draw_plot(xlabel_name = xlabel_name ,
                ylabel_name = ylabel_name,
                title_name = title_name)

    fig = plt.gcf()
    ax = fig.gca()

    for i , v in enumerate(batsman_all_stats.head(10)["average"].values):
        ax.text(10, i, v,fontsize=16,color='white',weight='bold')

    st.pyplot(fig)

def display_batsman_strike_rate(batsman_all_stats):
    batsman_all_stats = batsman_all_stats[batsman_all_stats["batsman_runs"] >= 300]
    batsman_all_stats = batsman_all_stats.sort_values(by ="strike_rate",ascending =False)
    xlabel_name = "average"
    ylabel_name = "Batsman"
    title_name = " Batsman strike rate Distribution"

    sns.barplot( x = "strike_rate" , y = "batsman" , data = batsman_all_stats.head(10), color = "brown")

    draw_plot(xlabel_name = xlabel_name ,
                ylabel_name = ylabel_name,
                title_name = title_name)

    fig = plt.gcf()
    ax = fig.gca()


    for i , v in enumerate(batsman_all_stats.head(10)["strike_rate"].values):
        ax.text(10, i, v,fontsize=16,color='white',weight='bold')
    
    st.pyplot(fig)

def display_batsman_milestone(batsman_milestone,milestone_name):
        batsman_milestone = batsman_milestone.sort_values(by =milestone_name,ascending =False)
        xlabel_name = str(milestone_name) + " milestones "
        ylabel_name = "Batsman"
        title_name = " Batsman " + str(milestone_name) + " Distribution "

        sns.barplot( x = milestone_name , y = "batsman" , data = batsman_milestone.head(10), 
        color = "blue")

        draw_plot(xlabel_name = xlabel_name ,
                    ylabel_name = ylabel_name,
                    title_name = title_name)

        fig = plt.gcf()
        ax = fig.gca()


        for i , v in enumerate(batsman_milestone.head(10)[milestone_name].values):
            ax.text(0.5, i, v,fontsize=16,color='white',weight='bold')
        
        st.pyplot(fig)

def display_CHT(batsman_all_stats):

    batsman_all_stats = batsman_all_stats.sort_values(by ="CHT",ascending =False)
    xlabel_name = "CHT"
    ylabel_name = "Batsman"
    title_name = " Batsman CHT Distribution"

    sns.barplot( x = "CHT" , y = "batsman" , data = batsman_all_stats.head(10), color = "green")

    draw_plot(xlabel_name = xlabel_name ,
                ylabel_name = ylabel_name,
                title_name = title_name)

    fig = plt.gcf()
    ax = fig.gca()


    for i , v in enumerate(batsman_all_stats.head(10)["CHT"].values):
        ax.text(0.5, i, v,fontsize=16,color='white',weight='bold')
    
    st.pyplot(fig)

def display_batsman_ranking(batsman_all_stats):

    st.markdown("<hr/>",unsafe_allow_html= True)
    title_page = "## The ranking of the best IPL " + str(ipl_season)+ " batsman"
    st.markdown(title_page)
    st.markdown("<hr/>",unsafe_allow_html= True)

    batsman_all_stats_6 = batsman_all_stats[['batsman_runs', 'batsman_fours',
       'batsman_six', 'average', 'strike_rate',"CHT"]]
    batsman_all_stats_6.index = batsman_all_stats["batsman"]

    from sklearn.preprocessing import scale
    X = pd.DataFrame(scale(batsman_all_stats_6), 
    index=batsman_all_stats_6.index, 
    columns=batsman_all_stats_6.columns)

    from sklearn.decomposition import PCA
    pca = PCA()
    df_plot = pd.DataFrame(pca.fit_transform(X), 
    columns=['PC1','PC2','PC3','PC4','PC5','PC6'], index=X.index)

    pca = PCA().fit(X)


    df_plot = df_plot.reset_index()
    df_plot = df_plot.sort_values(by = ["PC1","PC2"],ascending = False)

    st.table(df_plot.head(10))
    
    plt.figure(figsize=(10,7))
    plt.plot(np.cumsum(pca.explained_variance_ratio_), color='k', lw=2)
    plt.xlabel('Number of components')
    plt.ylabel('Total explained variance')

    plt.axhline(0.9, c='r')
    plt.show();
    fig = plt.gcf()
    st.pyplot(fig)

def display_bowling_average(bowler_stats):


    
    bowler_stats = bowler_stats.sort_values(by = "average",ascending = True)
    xlabel_name = "Average"
    ylabel_name = "Bowler"
    title_name = " Bowler Average Distribution [ Runs / Wickets ]"

    sns.barplot( x = "average" , y = "bowler" , data = bowler_stats.head(10), color = "blue")

    draw_plot(xlabel_name = xlabel_name ,
                ylabel_name = ylabel_name,
                title_name = title_name)

    fig = plt.gcf()
    ax = fig.gca()


    for i , v in enumerate(bowler_stats.head(10)["average"].values):
        ax.text(2, i, v,fontsize=16,color='white',weight='bold')

    st.pyplot(fig)

def display_most_wickets(bowler_stats):
    bowler_stats = bowler_stats.sort_values(by = "wickets",ascending = False)
    xlabel_name = "Wickets"
    ylabel_name = "Bowler"
    title_name = " Wickets taken by Bowler"

    sns.barplot( x = "wickets" , y = "bowler" , data = bowler_stats.head(10), color = "orange")

    draw_plot(xlabel_name = xlabel_name ,
                ylabel_name = ylabel_name,
                title_name = title_name)

    fig = plt.gcf()
    ax = fig.gca()


    for i , v in enumerate(bowler_stats.head(10)["wickets"].values):
        ax.text(2, i, v,fontsize=16,color='white',weight='bold')
    
    st.pyplot(fig)

def display_bowler_strike_rate(bowler_stats):
    bowler_stats = bowler_stats.sort_values(by = "strike_rate",
    ascending = True)
    xlabel_name = "strike_rate"
    ylabel_name = "Bowler"
    title_name = " Bowler Strike Rate Distribution [ Balls / Wickets ]"

    sns.barplot( x = "strike_rate" , y = "bowler" , data = bowler_stats.head(10), color = "maroon")

    draw_plot(xlabel_name = xlabel_name ,
                ylabel_name = ylabel_name,
                title_name = title_name)

    fig = plt.gcf()
    ax = fig.gca()

    for i , v in enumerate(bowler_stats.head(10)["strike_rate"].values):
        ax.text(2, i, v,fontsize=16,color='white',weight='bold')
    
    st.pyplot(fig)

def display_most_econ(bowler_stats):
    bowler_stats = bowler_stats.sort_values(by = "econ",ascending = True)
    xlabel_name = "econ"
    ylabel_name = "Bowler"
    title_name = " Bowler econ Distribution [ Runs / Over ]"

    sns.barplot( x = "econ" , y = "bowler" , data = bowler_stats.head(10), color = "red")

    draw_plot(xlabel_name = xlabel_name ,
                ylabel_name = ylabel_name,
                title_name = title_name)

    fig = plt.gcf()
    ax = fig.gca()


    for i , v in enumerate(bowler_stats.head(10)["econ"].values):
        ax.text(2, i, v,fontsize=16,color='white',weight='bold')
    
    st.pyplot(fig)

def display_bowler_ranking(bowler_stats):
    
    st.markdown("<hr/>",unsafe_allow_html= True)
    title_page = "## The ranking of the best IPL " + str(ipl_season)+ " bowler "
    st.markdown(title_page)
    st.markdown("<hr/>",unsafe_allow_html= True)

    bowler_stats = bowler_stats[bowler_stats["deliveries"] > bowler_stats["deliveries"].median()]
    bowler_all_stats_4 = bowler_stats[['wickets', 'average','strike_rate', 'econ']]

    bowler_all_stats_4 = bowler_all_stats_4.fillna(0)
    bowler_all_stats_4.index =bowler_stats.bowler

    from sklearn.preprocessing import scale
    X = pd.DataFrame(scale(bowler_all_stats_4), index=bowler_all_stats_4.index, columns=bowler_all_stats_4.columns)
    
    from sklearn.decomposition import PCA
    # Fit the PCA model and transform X to get the principal components
    pca = PCA()
    df_plot = pd.DataFrame(pca.fit_transform(X), columns=['PC1','PC2','PC3','PC4'], index=X.index)
    df_plot = df_plot.reset_index()
    df_plot = df_plot.sort_values(by = 'PC1',ascending = True).head(15)
    st.table(df_plot.head(10))

    pca = PCA().fit(X)

    plt.figure(figsize=(10,7))
    plt.plot(np.cumsum(pca.explained_variance_ratio_), color='k', lw=2)
    plt.xlabel('Number of components')
    plt.ylabel('Total explained variance')

    plt.axhline(0.95, c='r')
    fig = plt.gcf()
    st.pyplot(fig)

    

def display_bowling_stats(filename,ipl_season = ""):
    bowler_stats = cricstats.get_bowler_stats(filename,ipl_season)

    if strategy == "Best Average":
        display_bowling_average(bowler_stats)
    elif strategy == "Most Wickets":
        display_most_wickets(bowler_stats)
    elif strategy == "Best Strike Rate":
        display_bowler_strike_rate(bowler_stats)
    elif strategy == "Best Economy":
        display_most_econ(bowler_stats)
    elif strategy == "Bowler Ranking ( 4 dimensions )":
        display_bowler_ranking(bowler_stats)

filename = "all_matches_IPL.csv"
if ipl_season == "2021":
    filename = "ALL_2021_IPL_MATCHES_BALL_BY_BALL.csv"

display_category(filename,ipl_season)
display_bowling_stats(filename,ipl_season)
