#!/usr/bin/perl -w

use strict;
use utf8;
use warnings;

use SUB;
use Template;
use CGI;
use CGI::Session;


my $cgi = CGI->new();

SUB::closeSession();

print $cgi->redirect('home.cgi');