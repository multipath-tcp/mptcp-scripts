#!/bin/bash

# Script that checks, if we had a dirty-reboot.
# crontab-ed every hour

if [ -f $HOME/send_alert ]
then
	rm $HOME/send_alert
	mutt -s "mptcp.info.ucl.ac.be rebooted" -- christoph.paasch@uclouvain.be < $HOME/mail
fi

if [ -f $HOME/no_crontab ]
then
	rm $HOME/no_crontab
else
	mutt -s "mptcp.info.ucl.ac.be - crontab issue!!!" -- christoph.paasch@uclouvain.be < $HOME/mail
fi

