# Baseball3
 
Hi. Welcome to Baseball3. In this version, there are different kind of pitches, and balls in play are modeled much more precisely. Additionally, Aidan starts to learn that DataFrames might be helpful.

NOTE: Hitter and Pitcher mode kinda work. I mean they work they just aren't super user friendly, I never quite got the output right. GM Mode is fully functional, will require you to look at some .xlsx files for player recruitment. 

Please note that for making bids on free agents during open auctions you are looking for UserAuctions.xlsx not UserFA.xlsx, which was for the old FA format. The old FA format can be used by switching 'faFormat' in DirectoryWide.py from 2 to 1.


--- Description of Files ---

Baseball3.py - main file, startup

DirectoryWide.py - Collection of variables and functions that I wanted the freedom to call from anywhere without worrying about circular import statements.

Linked_List3.py - W&M241 project to build a linked list. I tinker it slightly and use it for the scoreboards in all my projects (best way I've come up with to be able to display extra innings).

Testing.py - All the tests to see if the game is balanced right and working how it's supposed to.

Tests.ipynb - Messing around with the DataFrames to make sure they were working right, just a lot easier to do in .ipynb tbh.

The rest I think do be what they do be. 


