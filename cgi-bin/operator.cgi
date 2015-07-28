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
my $operator_name = $cgi->param('name');

print $cgi->header( -type => "text/html", charset => 'utf-8', -status => "200 OK" );
print $cgi->start_html;

my @plans;

foreach my $node ($doc->findnodes("//$operator_name")){

	my $plan = {
		operator		=> $node->getName(),
		id				=> $node->findvalue('@xml:id'),
		payments		=> $node->findvalue('@payments'),
		title			=> $node->findvalue('title'),
		insertdatetime	=> $node->findvalue('insertdatetime'),
		available		=> $node->findvalue('available/@disabled'),
		startdate		=> $node->findvalue('available/startdate'),
		enddate			=> $node->findvalue('available/enddate'),
		currency		=> $node->findvalue('price/@currency'),
		price			=> $node->findvalue('price'),
		unit			=> $node->findvalue('expiry/@unit'),
		expiry			=> $node->findvalue('expiry'),
		minutes			=> $node->findvalue('rates/minutes'),
		messages		=> $node->findvalue('rates/messages'),
		datasize		=> $node->findvalue('rates/internet/@datasize'),
		internet		=> $node->findvalue('rates/internet'),
		description		=> $node->findvalue('description')
	};

	push(@plans, $plan);
}

my %data = (plans => \@plans);


my $template = Template->new();
my $template_file = 'templates/operator.tt';

$template->process($template_file, \%data) || die "Template process failed: ", $template->error(), "\n";

print $cgi->end_html;