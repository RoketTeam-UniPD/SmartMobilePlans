#!/usr/bin/perl -w


#direttive d'uso strette
use strict;
use utf8;
use warnings;


#importazioni librerie varie
use CGI;
use Digest::SHA qw(sha256_hex);
use CGI::Session;
use POSIX qw(strftime);
use Template;
use XML::LibXML;
#forse inutile use LWP::UserAgent;


# importazione funzioni comuni
use SUB;

# lettura del file contenente gli amministratori
my $parser = XML::LibXML->new();
my $doc = $parser->parse_file('../data/admins.xml');


# istanza del file
my $cgi = CGI->new();


# caricamento sessione attive se presenti
my $session = CGI::Session->load();

my $username;


# controllo se l'utente è già loggato
if ($session->param('user') ne undef) {

    $username = $session->param('user');

}else{  

    # recupero username e password passati
    $username = $cgi->param('username');
    $username =~ tr/a-zA-Z0-9//dc;
    my $pwd = $cgi->param('pwd');
    $pwd = sha256_hex($pwd);

    # controllo se esiste l'utente nella base di dati
    my $admin = $doc->findnodes("//admin[username='" . $username . "']");

    # se l'username non c'è o è vuoto
    if (!$admin || $username eq '') {
        #redirect con errore
        print $cgi->redirect('login.cgi?err=usr');
    } else {
        my $password = $admin->pop()->findvalue("./password");
        
        if ($password ne $pwd || $pwd eq '') {
            print $cgi->redirect('login.cgi?err=pwd');
        }

        # User exists, initialize session
        my $session = CGI::Session->new();
        $session->param('user', $username);
        print $session->header(-location=>"admin.cgi");
    } 
}


my %data = (
    username => $username, 
    curYear => (strftime "%Y", localtime),
    error => $cgi->param("e"),
    formData => $session->param("form-data"),    
);





# creazione header del file
print $cgi->header( -type => "text/html", charset => 'UTF-8', -status => "200 OK" );


# stampa header
print SUB::printStartHeader('Admin page of');


# stampa header HTML
print SUB::printHeaderSITE();


# stampa menu HTML
print SUB::printMenuSITE();


# stampa breadcrumbs HTML
my @breadcrumbs = (
    [ "Admin" ],
);

print SUB::printBreadcrumbsSITE(\@breadcrumbs);


# inizializzazione ed istanziazione del sitema di templating
my $template = Template->new();
my $template_file = 'templates/admin.tt';

$template->process($template_file, \%data) || die "Template process failed: ", $template->error(), "\n";

# stampa footer
print SUB::printFooterHTML();


# stampa chiusura header
print SUB::printCloseHeader();
