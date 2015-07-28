#!/usr/bin/perl -w

use strict;
use utf8;
use warnings;

use Data::Dumper;
use Template;
use XML::LibXML;
use LWP::UserAgent;
use CGI;


my $parser = XML::LibXML->new();
my $doc = $parser->parse_file('../data/admins.xml');


my $cgi = CGI->new();

print $cgi->header( -type => "text/html", charset => 'utf-8', -status => "200 OK" );
print $cgi->start_html;


# my $node = $doc->findnodes("//admin[username='']")


# TODO: order elements by date DESC
my $admin = {
	username => $cgi->param("username")
};

my $template = Template->new();
my $template_file = 'templates/admin.tt';

$template->process($template_file, $admin) || die "Template process failed: ", $template->error(), "\n";

print $cgi->end_html;