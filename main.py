import pwd
import tweepy
import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None
def tweet_search_clen(api):
    '''
    Location cordinates are stored in location list
    '''
    location = [(10.2188344, 92.5771329), (15.9240905, 80.1863809), (27.6891712, 96.4597226), (26.4073841, 93.2551303),
                (25.6440845, 85.906508), (30.7194022, 76.7646552), (21.6637359, 81.8406351),
                (20.713587, 70.92296517214575), (28.6517178, 77.2219388), (15.3004543, 74.0855134),
                (22.41540825, 72.03149703699282), (29.0, 76.0), (31.81676015, 77.34932051968858),
                (33.5574473, 75.06152), (23.4559809, 85.2557301), (14.5203896, 75.7223521), (10.3528744, 76.5120396),
                (33.9456407, 77.6568576),
                (10.8832771, 72.8171069), (23.9699282, 79.39486954625225), (19.531932, 76.0554568),
                (24.7208818, 93.9229386), (25.5379432, 91.2999102), (23.2146169, 92.8687612), (26.1630556, 94.5884911),
                (20.5431241, 84.6897321), (11.9340568, 79.8306447), (30.9293211, 75.5004841), (26.8105777, 73.7684549),
                (27.601029, 88.45413638680145), (10.9094334, 78.3665347), (17.8495919, 79.1151663),
                (23.7750823, 91.7025091), (27.1303344, 80.859666), (30.091993549999998, 79.32176659343018),
                (22.9964948, 87.6855882)]
    for state_index in range(len(location)):
        ntweet_list = []
        geocode = "%.5f" % location[state_index][0] + ',' + "%.5f" % location[state_index][1] + ",50km"

    '''
        query variable is having all the keywords to search from twitter
    '''
    query = "crypto" or "btc" or "bitcoin" or "#btc" or "#bitcoin" or "cryptocurrency" or "#crypto" or "#cryptocurrency" or "Ethereum" or "#Ethereum" or "Ethereum Classic" or "#EthereumClassic" or "Ripple" or "Litecoin" or "Polkadot" or "Bitcoin Cash" or "Dogecoin" or "Tron"

    newntweet = tweepy.Cursor(api.search_tweets, q=query, tweet_mode="extended", lang="en",result_type="recent" ,geocode=geocode).items(200)
    tweets = []
    like = []
    retweet = []
    hastg = []
    time = []
    hashtags = []
    for ntweet in newntweet:
        try:
            for hashtag in ntweet.entities.get('hashtags'):
                hashtags.append(hashtag["text"])
        except:
            pass
        c = 0;
        for i in hashtags:
            tweets.append(ntweet.full_text)
            like.append(ntweet.favorite_count)
            retweet.append(ntweet.retweet_count)
            time.append(ntweet.created_at)
            hastg.append(hashtags[c])
            c = c + 1
    df = {}
    df = pd.DataFrame({'hashtag': hastg, 'like': like, 'retweet': retweet, 'time': time})
    df['hashtag'] = df['hashtag'].str.lower()
    '''
    Removing the unwanted hashtags to filter only the cryptocurrency  and cleaning the anamolies
    '''
    df['hashtag'] = df[~df['hashtag'].isin(
        ['crypto', 'cryptocurrency', 'cryptocurrencies', 'cryptocoin', 'blockchain', 'coin', 'cryptonews',
         'cryptocurrencynews', 'digitalcurrency', 'digitalcoin', 'cryptography', 'coinstockexchange', 'cointrading',
         'giveaway', 'giveaways', 'coinswitch', 'money', 'technology', 'digitaltechnology', 'wazirx', 'wazir',
         'trading', 'cryptotrading'])]['hashtag']
    df = df.dropna()
    df = df.drop_duplicates()
    return df


# ntweet_df = df.reset_index(drop=True)
# print(ntweet_df)
# mostlike=df.loc[df.like.nlargest(5).index]
def trend_tweet(df):
    '''
    Finding the trending crypto
    '''
    df1 = df['like'] + df['retweet']
    df['trend_count'] = df1
    df2 = pd.DataFrame(df)
    # print(df2.loc[df2.trend_count.nlargest(5).index])

    df_count_hashtg = df.groupby('hashtag').agg(count_hashtg=('hashtag', 'count'))
    df7 = pd.DataFrame(df_count_hashtg)
    #df_max_hashtag_count = df7[df7.count_hashtg == df7.count_hashtg.max()]
    df_tr = df7.merge(df, on='hashtag', how='inner')
    df_tr['final_count']=df_tr['count_hashtg'] + df_tr['trend_count']
    df_max_trend1 = df_tr[df_tr.final_count == df_tr.final_count.max()]
    return df_max_trend1


def main():
    consumer_key = pwd.consumer_key
    consumer_secret = pwd.consumer_secret
    access_token = pwd.access_token
    access_token_secret = pwd.access_token_secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    df = tweet_search_clen(api)
    print("All Time Trending crpto currency")
    trend_tw = pd.DataFrame(trend_tweet(df)[['hashtag', 'like', 'retweet', 'trend_count','final_count']])
    print(trend_tw)
    max_time = max(df.time)
    time_5 = max_time - timedelta(minutes=5)
    time_10 = max_time - timedelta(minutes=10)
    time_30 = max_time - timedelta(minutes=30)

    df_5 = df[(df['time'] > time_5)]
    df_10 = df[(df['time'] > time_10)]
    df_30 = df[(df['time'] > time_30)]
    print('===========================================')
    print("Last 5 min trending crpto is ")
    print(trend_tweet(df_5))
    print('===========================================')
    print("Last 10 min trending crpto is ")
    print(trend_tweet(df_10))
    print('===========================================')
    print("Last half an hour trending crpto is ")
    print(trend_tweet(df_30))

    df1 = df['like'] + df['retweet']
    df['trend_count'] = df1
    result = df.groupby(["hashtag"])["hashtag"].count().reset_index(name="count_of_hashtag")
    # Plot horizontal bar graph for showing the trends of crypto
    fig, ax = plt.subplots(figsize=(8, 8))
    result.plot.barh(x='hashtag',
                             y='count_of_hashtag',
                             ax=ax,
                             color="Green")
    ax.set_title("Trending Cryptocurrencies")
    plt.show()

if __name__ == "__main__":
    main()