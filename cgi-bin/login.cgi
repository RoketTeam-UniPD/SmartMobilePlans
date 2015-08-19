#!/usr/bin/perl -w

use strict;
use utf8;
use warnings;

use Template;
use CGI;
use CGI::Session;


my $cgi = CGI->new();

my $session = CGI::Session->load();
if ($session->param('user') ne undef) {
	print $cgi->redirect('admin.cgi');
}

print $cgi->header( -type => "text/html", charset => 'utf-8', -status => "200 OK" );
print $cgi->start_html;


my $template = Template->new();
my $template_file = 'templates/login.tt';

$template->process($template_file, { error => $cgi->param('e') }) || die "Template process failed: ", $template->error(), "\n";

print $cgi->end_html;