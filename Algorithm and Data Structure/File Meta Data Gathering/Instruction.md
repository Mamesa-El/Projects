File Metadata Gathering
=======================
This is a tech screen exercise. It is very similar to a task we need to perform sometimes in our production environments.

You are provided with a collection of dummy sample text files. They are
available [here](https://github.com/jimmyislive/sample-files).

The task is to write a program (`file_metadata.py` or in golang) that provides us with a csv file (`interview.csv`) that contains the following information about these `sample_file_*.txt` files:

1. File name
2. Sha256 hexdigest of the file
3. File size
4. Word count
5. Number of unique words in this file
6. Todays date (In format YYYY-MM-DD)

The above information should be in a csv file called `interview.csv`. The File size should be provided in bytes. For the word count, assume that space is the delimiter between words.

E.g. the first line of your interview.csv would be:

`sample_file_0.txt, 89abab31bc4c08205ea4190cac98deb0b9844da121acff9de93ea41adade8a75, 371240, 32025, 29449, 2019-01-24`

No github creds are needed to programmatically access these files. Wrap this up in a docker container. The container should be named: `cs-<firstname>-<lastname>-file-metadata:0.0.1`. Provide us with a dockerfile so that we can build the  container, do a docker run command and it will deposit the `interview.csv` in the current directory. After we execute your `docker run` we should be able to see the answer by doing: `cat interview.csv`. Feel free to use all usual resources available on the internet as you would do in your normal working. As a request, please don't share your solution or ask others to do it for you !

NOTE: Don't git clone the sample-files repo. Programmatically pull the files down in your submission.

Please write this code as if you were doing it in a production peer-reviewed setting. Add anything you think is important and feel free to impress us ! 

Deliverable
-----------
   A zip / tgz file containing everything required for this assignment. Please include a `README.md` file giving details how to build, run, and test your container.

FAQ
---

1. Are we supposed to programmatically access these files thru the web eg make a web call to github to download these files      and process them or can we download them locally and include them in our docker?

   *The program has to programmatically download them via a web call. We will run your program and it should download when we     run as well.*