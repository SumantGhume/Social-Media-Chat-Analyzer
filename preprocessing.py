import pandas as pd
import re
def preprocess(data):
    dissision_pattern = "\d{1,2}:\d{2}\s[AaPp][Mm]"
    dission = len(re.findall(dissision_pattern, data))

    ## For 12-Hour Time Analysis
    if dission >= 3:
        pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[AaPp][Mm]\s-\s"
        pattern1 = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[AaPp][Mm]"
        messages = re.split(pattern, data)[1:]
        dates = re.findall(pattern1, data)

        data = pd.DataFrame({"user_message": messages, "date": dates})
        data["date"] = pd.to_datetime(data["date"], format="%d/%m/%Y, %I:%M %p")
        data = data[["date", "user_message"]]

    ## For 24-Hour Analysis
    else:
        pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

        messages = re.split(pattern, data)[1:]
        dates = re.findall(pattern, data)

        data = pd.DataFrame({'user_message': messages, 'date': dates})
        data['date'] = pd.to_datetime(data['date'], format='%d/%m/%Y, %H:%M - ')

        data = data[["date", "user_message"]]

    ## Seperating the user name and the message of the user.
    users = []
    messages = []
    for message in data['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))  # Converting the List of the user into a string.
        else:
            users.append('group_notification')
            messages.append(entry[0])

    data['user'] = users
    data['message'] = messages
    data.drop(columns=['user_message'], inplace=True)

    ## Forming columnsfor 'year' , 'months' , 'day' , 'hour' , 'minute'
    data['only_date'] = data['date'].dt.date
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.month_name()
    data['month_num'] = data['date'].dt.month
    data['day'] = data['date'].dt.day
    data['day_name'] = data['date'].dt.day_name()
    data['hour'] = data['date'].dt.hour
    data['minute'] = data['date'].dt.minute

    period = []
    for hour in data[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    data['period'] = period

    return data


