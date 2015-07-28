#!/usr/bin/perl -w

use strict;
use utf8;
use warnings;

use Data::Dumper;
use Template;
use XML::LibXML;
use CGI;


my $parser = XML::LibXML->new();
my $doc = $parser->parse_file('../data/plans.xml');


my $cgi = CGI->new();

print $cgi->header( -type => "text/html", charset => 'utf-8', -status => "200 OK" );
print $cgi->start_html;

my @plans;

foreach my $node ($doc->findnodes("/plans/child::*[position() < 6]")){

	my $plan = {
		# operator		=> $node->getName(),
		title			=> $node->findvalue('title'),
		insertdatetime	=> $node->findvalue('insertdatetime'),
		description		=> $node->findvalue('description')
	};

	push(@plans, $plan);
}

# TODO: order elements by date DESC

my %data = (plans => \@plans);


my $template = Template->new();
my $template_file = 'templates/login.tt';

$template->process($template_file, \%data) || die "Template process failed: ", $template->error(), "\n";

print $cgi->end_html;