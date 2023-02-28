
# Pyrogram-Add-Member

This Project Let You add members from Your group to another group or supergroup.

This project is most optimised Telegram member adder.


## Acknowledgements

- [Pyrogram](https://github.com/pyrogram/pyrogram)



## Authors

- [@saifalisew1508](https://www.github.com/saifalisew1508)


## Installation

- To deploy this project run you must have python3 installed and git
- use other command if first one give error 


```
Get Api_Id and Api_Hash From my.telegram.org
```
```
bash git clone https://github.com/saifalisew1508/TelegramAdderTool
```
```
 RUN pip3 install -r requirements.txt or pip -r install requirments.txt 
```
Now Add Accounts Which accounts be Used For Adding 
```
RUN python3 make_config.py or python make_config.py
```
- first  id of group you want to scrap
- second id of ur group
- source username is the link or username of group you want to scrap
- target username is the link or username of your group
- if you have api_id and hash for ur numbers type YES otherwise 

# To Do
if you did not add number in phone.csv you will be asked for 
how many numbers you want to add
- first add ur phone numbers in phone.csv (optional)
- type the number one by one with country code example 918571000000 [91 is my country code] (only required if you did not fill phone.csv)
# To Don't
-  enter number of account you want to add example: 10 or 5
-  enter ur number with country code example 919708973259 [91 is my country code]
-  enter ur api id. get from https://my.telegram.org/auth
-  enetr ur api hash. get from https://my.telegram.org/auth


### AutoJoin and SpamCheck accepts [True/false] editable in  config.py after you run make_confg.py

```
RUN python3 login.py or python login.py 
```
- Follow on screen instructions
- Don't use Bot token
```
RUN python3 get_data.py or python get_data.py
```
- this will extract 10k members from source group
- there are two option username or id 
- id will add more member but scraping take long
- username is best if you want to save time
```
RUN python3 add_member.py or python add_member.py
```
- member adding has started
- there two option username/id
- choose what you picked above
- dont missmatch pick it will give erros

## Features
### GitHub Version
- 10k members scraping 
- Faster speed
- skip admins
- skip bot
- auto check spambot
- add by username or id
- auto save last count
- Better Error Handling 
- auto_make config
- Unlimited account
- Account are used with sync so less wait time
- Cross platform
- First open source add member written in pyrogram 

### Premium Version
- all from GitHub
- scrap full group not just 10k
- 40-80 times faster
- use parallel get_data
- scraps contacts and save in .CSV file
- Setup help contact [@OpenSource_Chat](https://t.me/OpenSource_Chat) on telegram 


## Support or donation 

For Premium version it's 50USD [US] Contact, [@PrinceXofficial](http://t.me/PrinceXofficial) on Telegram

Or help and support [@OpenSource_Chat](https://t.me/OpenSource_Chat)


## FAQ

#### How Many Member 20 Account can add?

600 - 1000 Member daily

### Error on login.py

use correct username for channel

### Error on get_data.py

raise a issue or use telegram support

#### How Many Account are recommended 

I will Suggest 15 but depends on ur biggest

Buy account from : [@OpenSource_Chat](http://t.me/OpenSource_Chat) on Telegram

Check @spambot on Telegram if ur account is limited

#### 6th point from installation

option are
```
 UserStatus.LONG_AGO - User was seen long ago
 UserStatus.LAST_MONTH - User was seen last month
 UserStatus.LAST_WEEK - User was seen last week
 UserStatus.OFFLINE - User is offline
 UserStatus.RECENTLY - User was online recently
 UserStatus.ONLINE - User is online
 ```
 6th option add user who are online and 1st add all the user

other should be clear from name

#### Is There a Paid version Available?

Yes it's called donation version 

#### My ETH wallet address

0x0fBcb24DC8588c63bdbC126e2192aB609c7dF528

#### My BTC wallet address

bc1qgfqtujdmdeaky0n80rswnfv8p7x62shspfl9rc

## Contributing:

* Fork the repo on Github

* Clone the repo using `git clone addmember-telegram`

* Make changes and stage the files: `git add .`

* Commit the changes: `git commit -m "Changed a few things"`

* Push the changes to your Github repo: `git push -u origin main`

* Submit a pull request.

* Don't add feature writen in donation

* Don't sell the code 😅😡
