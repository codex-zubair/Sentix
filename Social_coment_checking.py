from pprint import pprint
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import praw


user_agent="Scraper 1.0 by /u/nokib_hassan_46"


reddit=praw.Reddit(
    client_id="ilG0OhYaigdAqGd1D90UvQ",
    client_secret="z78ZGGYN3-UKpIM3EuBCtmuqoGS-0g",
    user_agent=user_agent



)


#hot new rising top

headlines=set()
for submission in reddit.subreddit('politics').hot(limit=None):

    print(submission.title)
    print(submission.id)
    print(submission.author)
    print(submission.created_utc)
    print(submission.score)
    print(submission.upvote_ratio)
    print(submission.url)
    break
    headlines.add(submission.title)
    print(len(headlines))


    df=pd.DataFrame(headlines)
    df.head()


    df.to_csv('abcnews-date-text.csv',header=False,encoding='utf-8',index=false)

    import nltk

    nltk.download('vader_lexicon')



    from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA


    sia=SIA()

    results=[]


    for line in headlines:

        pol_score=sia.polarity_scores(line) #dict

        pol_score['headline']=line
        results.append(pol_score)


        pprint(results[:3],width=100)


        df=pd.DataFrame.from_records(results)
        df.head()



        df['label']=0
        df.loc[df['compound']>0.2,'label']=1
        df.loc[df['compound']<-0.2,'label']=-1
        df.head()



        df2 = df[['headline', 'label']]
        df2.to_csv('reddit_headlines_labels.csv', mode='a', encoding='utf-8', index=False)


        print(df.label.value_counts())

        print(df.label.value_counts(normalize=True) * 100)


        print("Positive headlines:\n")
        pprint(list(df[df['label'] == 1].headline)[:5], width=200)

        print("\nNegative headlines:\n")
        pprint(list(df[df['label'] == -1].headline)[:5], width=200)



        fig, ax = plt.subplots(figsize=(8, 8))

        counts = df.label.value_counts(normalize=True) * 100

        sns.barplot(x=counts.index, y=counts, ax=ax)

        ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])
        ax.set_ylabel("Percentage")

        plt.show()

