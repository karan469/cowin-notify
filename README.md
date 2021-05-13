# cowin-notify

## How to use
1. Create a channel on slack and register a channel heb hook, which allows the script to send message to that channel.
2. Store the channel hook uid which is at the end of https://hooks.slack.com/services/ (for example https://hooks.slack.com/services/AAAAA/BBBBB/CCCCC has the uid of channel hook AAAA/BBBB/CCCC)
3. Run the script locally.

## Examples: 
```python
  python3 test.py --pincode 110011 --minimum_age 18 --channel_hook AAAA/BBBB/CCCC
  python3 test.py --district_id 143 --minimum_age 45 --channel_hook AAAA/BBBB/CCCC
```

## Notes:
1. The script checks the slots every 3 seconds because of the limit of api calls per IP.
2. The script checks the slots from 7 days of the current date.
3. You can either set pincode, or district code to get notify accordingly.
4. If you want to customize your needs (like choosing only covaxin) you can modify the script accordingly.
5. District id list: https://github.com/bhattbhavesh91/cowin-vaccination-slot-availability/blob/main/district_mapping.csv

For any queries or feedback, raise an issue here or contact me at Instagram @_tanwar_karan 

Be safe and all the best :)
