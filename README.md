# Finance bot

Telegram bot with the task to categorize and write down all the spendings. 
## List of commands:
```
/categories — Show all available categories
/delete [id] — Delete the receipt with the ID
/delall — Delete all receipts for the current month
/statistic — Show expenses for the current month
/expenses — Show all categorized expenses
```
The template of receipt:
```
250 books
```
More explicitly: first place is reserved for the money that was spent, second place is the category that money was spent on.

## Requirements
Can be found in requirements.txt
### To install:
1. Git clone the repository
2. Create venv
3. Install all requirements
```
pip install -r requirements.txt
```
4. Create DB with PgAdmin querytool and createdb file
5. Create and fill .env file with environmental variables 
6. Create TG bot and then load it's ID to the env file
7. Ready to go
