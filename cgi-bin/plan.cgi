#!/usr/bin/perl -w


#direttive d'uso strette
use strict;
use utf8;
use warnings;


#importazioni librerie varie
use CGI;
use HTML::Entities;
use Template;
use XML::LibXML;
# da cancellare ? use LWP::UserAgent;

# importazione funzioni comuni
use SUB;


# lettura del file
my $parser = XML::LibXML->new();
my $doc = $parser->parse_file('../data/plans.xml');


# istanza del file
my $cgi = CGI->new();


my $id = $cgi->param('id');


# Get element from id
my $node = $doc->findnodes(qq(//*[\@id="$id"]))->pop();


# Conversione per la visualizzazione corretta in HTML
my $desc = $node->findvalue('description');
my $description = decode_entities($desc);
my $insertdatetime = $node->findvalue('insertdatetime');
$insertdatetime =~ s/T/ /g;



# Fill var to send an template file
my $plan = {
	operator		=> $node->getName(),
	id				=> $node->findvalue('@id'),
	payments		=> $node->findvalue('@payments'),
	title			=> $node->findvalue('title'),
	insertdatetime	=> $insertdatetime,
	startdate		=> $node->findvalue('available/startdate'),
	enddate			=> $node->findvalue('available/enddate'),
	currency		=> $node->findvalue('price/@currency'),
	price			=> decode_entities($node->findvalue('price')),
	unit			=> $node->findvalue('expiry/@unit'),
	expiry			=> $node->findvalue('expiry'),
	minutes			=> decode_entities($node->findvalue('rates/minutes')),
	messages		=> decode_entities($node->findvalue('rates/messages')),
	datasize		=> decode_entities($node->findvalue('rates/internet/@datasize')),
	internet		=> decode_entities($node->findvalue('rates/internet')),
	description		=> "$description"
};


# se non vi è nessun id corrispondente si viene redirettati
if (!defined $node){
	print $cgi->redirect('../404.html');
	exit;
}else{
	# creazione header del file
	print $cgi->header( -type => "text/html", charset => 'UTF-8', -status => "200 OK" );
}


# stampa header
my $siteTitle = "$plan->{'title'} plan of ".uc($plan->{'operator'})." operator -";
print SUB::printStartHeader("$siteTitle");


# stampa header HTML
print SUB::printHeaderSITE();


# stampa menu HTML
print SUB::printMenuSITE($plan->{'operator'});


# stampa breadcrumbs HTML
my @breadcrumbs = (
    [ "Home", "home.cgi" ],
    [ "$plan->{'operator'}", "operator.cgi?name=$plan->{'operator'}" ],
    [ "$plan->{'title'} " ],
);

print SUB::printBreadcrumbsSITE(\@breadcrumbs);


# inizializzazione ed istanziazione del sitema di templating
my $template = Template->new();
my $template_file = 'templates/plan.tt';

$template->process($template_file, $plan) || die "Template process failed: ", $template->error(), "\n";


# stampa footer
print SUB::printFooterHTML();


# stampa chiusura header
print SUB::printCloseHeader();

