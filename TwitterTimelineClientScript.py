# /etc/bin/python3
import datetime
import tweepy
import sys,os
import csv
import json
import requests
import argparse
import pytz



# API验证信息
API_KEY = ""
API_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
BEARER_TOKEN = ""

# 登入API
auth = tweepy.OAuthHandler(API_KEY,API_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# 时间修正
tz = pytz.timezone('Asia/Shanghai')

# 读取twitter用户时间线
def tweepy_from_usernamefile(username_file_path,limit,output):
    try:
        feedtwitter = open(username_file_path)
        csvlogFile=open("./logs/Usernamefile-tweepytask-"+str(datetime.datetime.now(tz).strftime("%Y-%m-%d_%H%M%S"))+".csv","a+",newline="",encoding="utf_8_sig")
        csvlogFileWriter = csv.writer(csvlogFile)
        try:
            csvFile= open(output,"a+",newline="",encoding="utf_8_sig")
            csvWriter = csv.writer(csvFile)
        except:pass
        for line in feedtwitter.readlines():
            UserName=line
            print(UserName)
            for tweet in tweepy.Cursor(api.user_timeline,screen_name=UserName,count=8000).items(limit):
                CN_timezone = (datetime.datetime.strptime(str(tweet.created_at), "%Y-%m-%d %H:%M:%S+00:00")+ datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S+0800")
                tweets = [tweet.text.encode("utf-8").decode(),CN_timezone]
                print(tweets)
                try:csvWriter.writerow(tweets)
                except:pass
                csvlogFileWriter.writerow(tweets)
    except Exception as error:
        print(error)
def tweepy_from_username(UserName,limit,output):
    try:
        csvlogFile=open("./logs/"+UserName+"-tweepytask-"+str(datetime.datetime.now(tz).strftime("%Y-%m-%d_%H%M%S"))+".csv","a+",newline="",encoding="utf_8_sig")
        csvlogFileWriter = csv.writer(csvlogFile)
        try:
            csvFile= open(output,"a+",newline="",encoding="utf_8_sig")
            csvWriter = csv.writer(csvFile)
        except:pass
        print(UserName)
        for tweet in tweepy.Cursor(api.user_timeline,screen_name=UserName,count=8000).items(limit):
            CN_timezone = (datetime.datetime.strptime(str(tweet.created_at), "%Y-%m-%d %H:%M:%S+00:00")+ datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S+0800")
            tweets = [tweet.text.encode("utf_8").decode(),CN_timezone]
            print(tweets)
            try:csvWriter.writerow(tweets)
            except:pass
            csvlogFileWriter.writerow(tweets)
    except Exception as error:
        print(error)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Twitter Api for read twitters.by x7peeps.com \n                           community v0.1 ')
    parser.add_argument('-f','--filepath',help='读取文件中的username',metavar="/yourpath/twitter_name_file.txt",default="") 
    parser.add_argument('-u','--username',help='指定一个username查询twitter信息',metavar="elonmusk",default="")
    parser.add_argument('-l','--limit',help='限制查询的数量',metavar="5",type=int,default=10)
    parser.add_argument('-o','--output',help='当使用-f批量查询的时候，可以指定一个导出路径',metavar="/yourpath/twitter_results_output.csv",default="") 
    parser.print_help()
    args = parser.parse_args()
    username_file_path=args.filepath
    username=args.username
    limit=args.limit
    output=args.output
    if username != "":
        tweepy_from_username(username,limit,output)
        sys.exit()
    if username_file_path !="":
        tweepy_from_usernamefile(username_file_path,limit,output)
        sys.exit()