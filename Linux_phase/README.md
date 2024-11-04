# My Linux Command Line Capture The Flag Journey

Welcome! This guide shows my journey through the seven challenges of the Linux Command Line Capture The Flag program. Each challenge was designed to test different aspects of my Linux skills. Remember, all flags are in the format `CTF{some_text_here}`.

## Environment Setup

This CTF challenge required me to deploy a lab environment in my preferred cloud provider. Everything was automated, and I followed the individual guides to set up the environment before proceeding with the CTF Challenges. I started by cloning the ltc-linux-challenge repo and running the terraform file in aws/ .

```sh
git clone https://github.com/learntocloud/ltc-linux-challenge

cd aws/

terraform apply
```

## Challenge 1: The Hidden File

![](/assets/Challenge_1-hiddenfile.png)

**Objective:** Find a hidden file in the `ctf_challenges` directory and read its contents.

**Skills tested:**

- Understanding of hidden files in Linux
- Using `ls` with appropriate flags
- Reading file contents

I used ```ls -la``` to find the hidden file and used ```cat``` command to display the flag

## Challenge 2: The Secret File
![](/assets/Challenge_2-thesecretfile.png)
**Objective:** Locate a file with the word "secret" in its name anywhere in the /home/ctf_user directory.

**Skills tested:**

- Recursive file searching
- Using grep or find commands

I used the ```find``` command to search for the file 

## Challenge 3: The Largest Log
![](/assets/Challenge_3-thelargestlog.png)
**Objective:** Find the largest file in the /var/log directory and retrieve the flag from it.

**Skills tested:**

- Navigating directory structures
- Sorting and filtering files based on size
- Reading file contents

I used ```du -hs /var/log/* | sort -h ``` command to list the files & dir with their disk space and sort them for easy readability. I found two large files cloud-init-output.log and large_log_file.log. I used the ``` grep ``` command to find the "CTF" text inside the large_log_file.log file and found the flag.  
    
      

## Challenge 4: The User Detective
![](/assets/Challenge_4-theuserdetective.png)

**Objective:** Identify the user with UID 1001 and find the flag in their home directory.

**Skills tested:**

- Understanding user management in Linux
- Reading the /etc/passwd file or using id command
- Navigating to other users' home directories

I used ```grep``` to search for the UID 1001 in the /etc/passwd.
I found the **ctf_user** but I could not cd into this directory even with sudo. I decided to list the files using sudo and was able to find the flag.txt which i ```cat``` and found the challenge 4 flag.



## Challenge 5: The Permissive File

![](/assets/Challenge_5-thepermissivefile.png)
**Objective:** Locate the file owned by root with permissions 777 and read its contents.

**Skills tested:**

- Understanding Linux file permissions
- Using find command with permission parameters
- Reading file contents as a non-root user

I used the ```find ``` command to look for a file ```-type f``` from root ```/``` with full permissions ```-perm 777```. I then ```cat`` the file and found the flag

## Challenge 6: The Hidden Service
![](/assets/Challenge_6-thehiddenservice.png)
**Objective:** Find the process running on port 8080 and retrieve the flag from its command.

**Skills tested:**

- Using network-related commands (netstat, ss, or lsof)
- Understanding process information
- Reading process details

I used ```netstat``` to show any tcp/udp connections or listening sockets. then used grep to search through the output and find **:8080**. I retrieved the flag from curling **localhost:8080**

## Challenge 7: The Encoded Secret
![](/assets/Challenge_7-theencodedsecret.png)
**Objective:** Decode the base64 encoded flag in the 'encoded_flag.txt' file.

**Skills tested:**

- Understanding of base64 encoding
- Using command-line decoding tools

I used ```find``` command to find the encoded file, then used the inbuilt ```base64 --decode ``` command to decode the file. I used echo for an easy to see formating.

