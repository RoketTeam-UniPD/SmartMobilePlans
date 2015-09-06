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


foreach my $node ($doc->findnodes("/plans/child::*[position() > last()-5]")){


    # Conversione per la visualizzazione corretta in HTML
    my $description = $node->findvalue('description');
    my $description = encode_entities($description);

    my $plan = {
        id              => $node->findvalue('@xml:id'),
        title           => $node->findvalue('title'),
        insertdatetime  => $node->findvalue('insertdatetime'),
        description     => $description,
    };

    push(@plans, $plan);
}

my @reversePlans = reverse(@plans);

# TODO: order elements by date DESC
my %data = (plans => \@reversePlans);


# inizializzazione ed istanziazione del sitema di templating
my $template = Template->new();
my $template_file = 'templates/home.tt';

$template->process($template_file, \%data) || die "Template process failed: ", $template->error(), "\n";


# stampa footer
print SUB::printFooterHTML();


# stampa chiusura header
print SUB::printCloseHeader();
