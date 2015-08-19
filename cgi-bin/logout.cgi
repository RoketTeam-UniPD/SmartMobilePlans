#!/usr/bin/perl -w

use strict;
use utf8;
use warnings;

use Template;
use CGI;
use CGI::Session;


my $cgi = CGI->new();

my $session = CGI::Session->load();
$session->close();
$session->delete();
$session->flush();

print $cgi->redirect('home.cgi');