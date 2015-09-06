#!/usr/bin/perl -w


#direttive d'uso strette
use strict;
use utf8;
use warnings;


#importazioni librerie varie
use CGI;
use CGI::Session;
use Template;


# importazione funzioni comuni
use SUB;


# istanza del file
my $cgi = CGI->new();


# caricamento sessione attive
my $session = CGI::Session->load();


# check se l'utente è già loggato
if ($session->param('user') ne undef) {
    print $cgi->redirect('admin.cgi');
}


# creazione header del file
print $cgi->header( -type => "text/html", charset => 'UTF-8', -status => "200 OK" );


# stampa header
print SUB::printStartHeader('Login area of');


# stampa header HTML
print SUB::printHeaderSITE();


# stampa menu HTML
print SUB::printMenuSITE();


# stampa breadcrumbs HTML
my @breadcrumbs = (
    [ "Login" ],
);

print SUB::printBreadcrumbsSITE(\@breadcrumbs);


# inizializzazione ed istanziazione del sitema di templating
my $template = Template->new();
my $template_file = 'templates/login.tt';

$template->process($template_file, { error => $cgi->param('e') }) || die "Template process failed: ", $template->error(), "\n";


# stampa footer
print SUB::printFooterHTML();


# stampa chiusura header
print SUB::printCloseHeader();
