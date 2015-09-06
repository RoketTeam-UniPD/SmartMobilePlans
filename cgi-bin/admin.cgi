#!/usr/bin/perl -w

use strict;
use utf8;
use warnings;

use CGI;
use Template;
use CGI::Session;
use XML::LibXML;
use LWP::UserAgent;
use POSIX qw(strftime);
use Digest::SHA qw(sha256_hex);



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
    error => $cgi->param("e"),
    curYear => "2015",
    formData => $session->param("form-data"),
    strftime "%Y", localtime,
);

print $cgi->header( -type => "text/html", charset => 'utf-8', -status => "200 OK" );

my $template = Template->new();
my $template_file = 'templates/admin.tt';

$template->process($template_file, \%data) || die "Template process failed: ", $template->error(), "\n";