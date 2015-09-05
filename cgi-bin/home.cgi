#!/usr/bin/perl -w


#direttive d'uso strette
use strict;
use utf8;
use warnings;


#importazioni librerie varie
use CGI;
use Data::Dumper;
use DateTime::Format::Strptime;
use DateTime::Format::ISO8601;
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


# creazione header del file
print $cgi->header( -type => "text/html", charset => 'UTF-8', -status => "200 OK" );


# stampa header
print SUB::printStartHeader('Homepage of');


# stampa header HTML
print SUB::printHeaderSITE();


# stampa menu HTML
print SUB::printMenuSITE('home');


# stampa breadcrumbs HTML
my @breadcrumbs = (
    [ "Home" ],
);

print SUB::printBreadcrumbsSITE(\@breadcrumbs);


# trova gli ultimi 5 piani inseriti e li visualizza
my @plans;


foreach my $node ($doc->findnodes("/plans/child::*[position() < 6]")){

    # Conversione per una data in formato più pretty
    my $dt = DateTime::Format::ISO8601->parse_datetime($node->findvalue('insertdatetime'));
    
    # Conversione per la visualizzazione corretta in HTML
    my $description = $node->findvalue('description');
    my $description = encode_entities($description);

    my $plan = {
        id              => $node->findvalue('@xml:id'),
        title           => $node->findvalue('title'),
        insertdatetime  => $dt,
        insertdatetime  => $dt->strftime('%H:%M:%S %d-%m-%Y'),
        description     => $description,
    };

    push(@plans, $plan);
}

# TODO: order elements by date DESC
my %data = (plans => \@plans);


# inizializzazione ed istanziazione del sitema di templating
my $template = Template->new();
my $template_file = 'templates/home.tt';

$template->process($template_file, \%data) || die "Template process failed: ", $template->error(), "\n";


# stampa footer
print SUB::printFooterHTML();


# stampa chiusura header
print SUB::printCloseHeader();
