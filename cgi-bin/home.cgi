#!/usr/bin/perl -w


#direttive d'uso strette
use strict;
use utf8;
use warnings;

#importazioni librerie varie
use CGI;
use Data::Dumper;
use Template;
use XML::LibXML;

# importazione funzioni comuni
use SUB;


# lettura del file
my $parser = XML::LibXML->new();
my $doc = $parser->parse_file('../data/plans.xml');


# istanza del file
my $cgi = CGI->new();


# creazione header del file
print $cgi->header( -type => "text/html", charset => 'utf-8', -status => "200 OK" );


# stampa header
print SUB::printHeader('Home');

# stampa header HTML
print SUB::printHeaderSITE();

# stampa menu HTML
print SUB::printMenuSITE('home');


# stampa breadcrumbs HTML
my @aaa = (
	[ "home", "home.cgi"],
	#[ "add", "add.cgi"],
);

print SUB::printBreadcrumbsSITE(\@aaa);




my @plans;

foreach my $node ($doc->findnodes("/plans/child::*[position() < 6]")){

	my $plan = {
		# operator		=> $node->getName(),
		id				=> $node->findvalue('@xml:id'),
		title			=> $node->findvalue('title'),
		insertdatetime	=> $node->findvalue('insertdatetime'),
		description		=> $node->findvalue('description')
	};

	push(@plans, $plan);
}

# TODO: order elements by date DESC

my %data = (plans => \@plans);


my $template = Template->new();
my $template_file = 'templates/home.tt';

$template->process($template_file, \%data) || die "Template process failed: ", $template->error(), "\n";
