
The assignment (trial)
----------------------
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



Result
------
conversion made by using russian ruble rate got from http://www.cbr.ru/
That site simple not required registration to get rates.
But, I think is not useful in production.



Notes about assignment
----------------------
The assignment is not clean to my look: REST is definition for service which operate some resources, but there is no resources, but exists some action: convertation from one currency to another currency. This case close to defenition RPC (over HTTP). So I don't know which http-verb useful in that case and used simple GET.

