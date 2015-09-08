#!/usr/bin/perl -w


#direttive d'uso strette
use strict;
use utf8;
use warnings;


#importazioni librerie varie
use CGI;
use Data::Dumper;
use HTML::Entities;
use Template;
use XML::LibXML;


# importazione funzioni comuni
use SUB;


# lettura del file
my $parser = XML::LibXML->new();
my $doc = $parser->parse_file('../data/plans.xml');


# istanza del file
my $cgi = CGI->new();


# parametro ricevuto contenente l'operatore
my $operator_name = $cgi->param('name');


# creazione header del file
print $cgi->header( -type => "text/html", charset => 'UTF-8', -status => "200 OK" );


# stampa header
my $siteTitle = (uc$operator_name)."'s plans -";
print SUB::printStartHeader("$siteTitle");


# stampa header HTML
print SUB::printHeaderSITE();


# stampa menu HTML
print SUB::printMenuSITE("$operator_name");


# stampa breadcrumbs HTML
my @breadcrumbs = (
    [ "$operator_name" ],
);

print SUB::printBreadcrumbsSITE(\@breadcrumbs);


# reaccolta di tutti 
my @plans;

foreach my $node ($doc->findnodes("//$operator_name")){

	my $plan = {
		operator		=> $node->getName(),
		id				=> $node->findvalue('@id'),
		title			=> $node->findvalue('title'),
		currency		=> $node->findvalue('price/@currency'),
		price			=> $node->findvalue('price'),
		minutes			=> $node->findvalue('rates/minutes'),
		messages		=> $node->findvalue('rates/messages'),
		datasize		=> $node->findvalue('rates/internet/@datasize'),
		internet		=> $node->findvalue('rates/internet'),
	};

	push(@plans, $plan);
}

my %data = (plans => \@plans, operator_name => $operator_name);


# inizializzazione ed istanziazione del sitema di templating
my $template = Template->new();
my $template_file = 'templates/operator.tt';

$template->process($template_file, \%data) || die "Template process failed: ", $template->error(), "\n";


# stampa footer
print SUB::printFooterHTML();


# stampa chiusura header
print SUB::printCloseHeader();