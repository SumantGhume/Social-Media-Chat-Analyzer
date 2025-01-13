import pandas as pd
from collections import Counter
from urlextract import URLExtract
from wordcloud import WordCloud
import emoji

extract = URLExtract()
def fetch_stats(selected_data, data):
    if selected_data != "Overall":
        data = data[data["user"] == selected_data]

    num_messages = data.shape[0]
    num_media_messages = data[data['message'] == '<Media omitted>\n'].shape[0]

    link = []
    for message in data["message"]:
        link.extend(extract.find_urls(message))

    words = []
    for message in data["message"]:
        words.extend(message.split())

    return num_messages, len(words), num_media_messages, len(link)

def fetch_most_active_user (data):
    x = data['user'].value_counts().head()

    result = round((data["user"].value_counts() / data.shape[0]) * 100, 1).reset_index().rename({"index": "user", "user": "perentage"})

    return x, result

def created_word_cloud(selected_user,data):
    if selected_user != 'Overall' :
        data = data[data['user'] == selected_user]
    temp = data[data['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    wc = WordCloud(width=500 , height= 500, min_font_size= 10 , background_color= 'white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def created_word_cloud_without_stop_words(selected_user , data) :
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]
    temp = data[data['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, data):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]
    temp = data[data['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message']!= 'This message was deleted\n']

    words  = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_words_data = pd.DataFrame(Counter(words).most_common(20))
    return most_common_words_data

def emoji_helper(selected_user, data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    emojis = []
    for message in data['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_counts = Counter(emojis)
    if len(emoji_counts) == 0:
        return pd.DataFrame(columns=['emoji' , 'count'])
    emoji_df= pd.DataFrame(emoji_counts.most_common() , columns=['emoji' , 'count'])
    return emoji_df

def montly_timeline(selected_user,data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    timeline = data.groupby(['year', 'month_num','month']).count()['message'].reset_index()

    time =[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user, data) :
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user ]

    daily_timeline = data.groupby('only_date').count()['message'].reset_index()

    return  daily_timeline

def monthly_activity_map(selected_user , data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    return data['month'].value_counts()

def weekly_activity_map(selected_user , data) :
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]
    return data['day_name'].value_counts()



def activity_heatmap(selected_user,data):

    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    user_heatmap = data.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap


