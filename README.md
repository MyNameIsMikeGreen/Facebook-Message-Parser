# Facebook-Message-Parser
[![Build Status](https://api.travis-ci.com/mikegreen1995/Facebook-Message-Parser.svg?branch=master)](https://travis-ci.com/mikegreen1995/Facebook-Message-Parser)

## What Does This Program Do?
Given a Facebook archive, this program will convert the messaging section of it into an SQLite database. This allows you to run queries on the message data for whatever reasons you have.

## What is a Facebook Archive?
Facebook allows you to download a copy of your data. You do this somewhere in your account settings (It changes, so there is little point in me instructing you here). This data dump can be in one of two formats as of writing this; HTML or JSON. I have chosen to refer to these data dumps as 'Facebook Archives' throughout this project.

## What is SQL and what is a query?
If you have these questions, you are not the target audience of this project.

## Which Archive Versions are Supported?
As of 2018, Facebook has overhauled the format of their data archive dumps. This project has been updated to support this new format exclusively. If you require compatibility with the pre-2018 format, you may try the [v1.0.0 release](https://github.com/mikegreen1995/Facebook-Message-Parser/releases/tag/v1.0.0) but this version is not maintained.

The JSON version of the archives are highly recommended over the HTML versions. The majority of the development effort is focused on this variant.

## Why Don't You Use the Facebook Messaging API?
APIs come and go. APIs change. Servers have downtime. A solar flare could take down the internet. But one thing is certain: as long as that solar flare didn't wipe out your entire country, and you still have your favourite Facebook archive handy, you can always run this program to satisfy all your post-apocalyptic querying needs!

## How do I Run it? 
``` python3 messageparser.py [path_to_your_archive]```

## How do I Run a Query?
There is no fancy way of doing this within the program currently. You can just use the utility functions provided and throw a query into the end of the main function, or you could output the database to a file using the `--output` flag and use some third-party tool to run queries.

## Your Program [Doesn't Work] / [Broke My Archive] / [Killed My Cat] / [Cured My Arthritis]!
This is supplied for free and completely without guarantee. Check the code before you run it if you are concerned. I accept no responsibility for anything that happens as a result of running this program.