
The assignment (trial)

Write a REST web service for currency conversion.

Exchange rates might be taken from free sources (e.g. https://openexchangerates.org/) and should be updated once a day. The rates should be stored in a database.

User interface design is not important and up to you.

Currencies:
Czech koruna
Euro
Polish złoty
US dollar.
The application should be tested as well. Code coverage is important.

The project should be uploaded to GitHub/Bitbucket.


Result:
convertation made by using russian ruble rate got from http://www.cbr.ru/
Setup notes:

You need provide call update_rates.sh from crontab everyday. For example call 'crontab -e' and in editor add line (replacing PROJECT_PATH to the project path)

0 5 * * * PROJECT_PATH/update_rates.sh

Or if you use virtual environment than you need to update update_rates.sh script to add virtualenv activation.

The assignment is not clean to my look: REST is defenotion for service which operate some resources, but there is no resources, but exists some action: convertation from one currency to another currency. This case close to defenition RPC (over HTTP). So I don't know which http-verb useful in that case and used sipmle GET.

