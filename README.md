# Suggestforme
Whenever you search for anime suggestions in google tired of getting the same results over and over again and results showing the ones you already have watched.This website helps you get new anime suggestions and get rid of the repetion cycle and endless search for new anime.
Website keeps track of which anime you have watched and will not suggest it,we can search for suggestions in specific genre.This app can be scaled to include books,movies,songs or even apps but for now its for anime only. Motivation for this website was that whenever i search for anime same results shows up like the top 20 anime again and again.
# Security Pratices:
Implemented email verification while signing up for first time,Thanks to Nithin Sharma for Django_verify_email module [https://github.com/foo290/Django-Verify-Email],
Email verification link expiration after some time,
Time based session logout,
Rate limiting password reset,
Django forms automatically sanitize the inputs,Parameterized Queries to prevent sql injection,html escaping and csrf tokens to prevent XSS attacks. 