import streamlit as st
import preprocessing
import HeplerFile
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyser')

## Uploading the .txt file
upload_file = st.sidebar.file_uploader("Upload your Whatsapp File in txt format", type='txt')

## Reading the File

if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode('utf-8')
    data = preprocessing.preprocess(data)
    ## Not displaying the dataframe in the webpage .
    st.dataframe(data)

## To seperate the name of the users from the user column and also forming Overall as a category for Analysis including th seperate user
    user_list = data["user"].unique().tolist()
    user_list.sort()
    user_list.remove("group_notification")
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox('Which user would you like to see Analysis(Select and Click Show Analysis button)', (user_list))

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, link = HeplerFile.fetch_stats(selected_user, data)

        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Total Messages Contributed by {}".format(selected_user))
            st.title(num_messages)

        with col2:
            st.subheader("Total Words of Messages by {}".format(selected_user))
            st.title(words)

        with col3:
            st.subheader("Total Media Shared by {}".format(selected_user))
            st.title(num_media_messages)

        with col4:
            st.subheader("Total Link Shared by {}".format(selected_user))
            st.title(link)

    ## Monthly Active Users
        st.title('Monthly Timeline')
        timeline = HeplerFile.montly_timeline(selected_user, data)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'] , color = 'red')
        plt.xticks(rotation = 90)
        plt.xlabel('Month - Year ')
        plt.ylabel('No.of Messages')
        st.pyplot(fig)

    ## Daily Active User
        st.title('Daily Timeline')
        daily_timeline = HeplerFile.daily_timeline(selected_user, data)
        fig , ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'] , color = 'green')
        plt.xticks(rotation=90)
        plt.xlabel('Date')
        plt.ylabel('No.of Messages')
        st.pyplot(fig)

    ## Activity Map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1 :
            st.header('Most Busy Day')
            busy_day = HeplerFile.weekly_activity_map(selected_user, data)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index , busy_day.values , color = 'purple')
            plt.xticks(rotation = 90)
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = HeplerFile.monthly_activity_map(selected_user, data)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

## Weekly Activity Map
        st.title('Weekly Activity HeatMap')
        user_heatmap = HeplerFile.activity_heatmap(selected_user, data)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        plt.xlabel('Time Gaps(in 24-Hours)')
        plt.ylabel('Days of the Week')
        st.pyplot(fig)


## Top 5 Most Active user
        if selected_user == 'Overall':
            st.subheader('Top 5 most active user and the percentage of contribution')
            x,percent_data = HeplerFile.fetch_most_active_user(data)
            fig ,ax = plt.subplots()
            col1 , col2 = st.columns(2)
            with col1 :
                ax.bar(x.index ,x.values , color= 'red')
                plt.xticks(rotation = 90)
                st.pyplot(fig)

            with col2 :
                st.dataframe(percent_data)
## For word cloud with stop words
        st.subheader("Word Cloud with stop words for {}".format(selected_user))
        wc_image = HeplerFile.created_word_cloud(selected_user, data)

        fig, ax = plt.subplots()
        ax.imshow(wc_image)
        st.pyplot(fig)

## For wordcloud with no stop words
        st.subheader("Word Cloud without stop words for {}".format(selected_user))
        wc_image = HeplerFile.created_word_cloud_without_stop_words(selected_user, data)

        fig, ax = plt.subplots()
        ax.imshow(wc_image)
        st.pyplot(fig)

## For most common words
        most_common_data = HeplerFile.most_common_words(selected_user, data)
        fig, ax = plt.subplots()
        ax.barh(most_common_data[0], most_common_data[1])
        plt.xticks(rotation=90)
        st.subheader("Most Comman Words Used by {}".format(selected_user))
        st.pyplot(fig)

## For emojis analysis
        emoji_df = HeplerFile.emoji_helper(selected_user , data)
        st.title('Emoji Analysis')

        col1, col2 = st.columns(2)
        with col1:
            if emoji_df.empty:
                st.write("No emojis found in the data.")
            else:
                st.dataframe(emoji_df)  # Display emoji DataFram
        with col2:
            if not emoji_df.empty:
                fig, ax = plt.subplots()  # Create a matplotlib figure
                    # Plot pie chart using the top emojis
                ax.pie(emoji_df['count'].head(), labels=emoji_df['emoji'].head(), autopct="%0.2f")
                st.pyplot(fig)  # Display the pie chart in Streamlit
            else:
                st.write("No emojis to display in the pie chart.")

