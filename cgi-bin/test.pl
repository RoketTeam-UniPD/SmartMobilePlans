#!/usr/bin/perl -w
#se metto un'opzione, l'eventuale Carriage Return rimane "attaccato" solo ad essa e non rischio messaggi di bad interpreter

#probalmente fanno gia`parte della configurazione di mod_perl #use CGI::Carp;
use CGI::Carp qw(carpout);
#use CGI::Carp qw(fatalsToBrowser); #in fase di consegna potrebbe bastare questo
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);

use CGI qw(:standard);
use CGI::Session;
use Apache::Session;

#da http://search.cpan.org/~gaas/libwww-perl-5.825/lib/LWP/Simple.pm #Note that if you are using both LWP::Simple and the very popular CGI.pm module, you may be importing a head function from each module, producing a warning like "Prototype mismatch: sub main::head ($) vs none". Get around this problem by just not importing LWP::Simple's head function, like so:                                        
use LWP::Simple qw(!head); 
#use WWW::Mechanize ;                                                                                                                                                                                               

use XML::Simple;
use XML::LibXML;

use XML::Writer ;
use XML::Handler::YAWriter;

use XML::XSLT;   #incompleta, meglio LibXSLT
use XML::LibXSLT;

use HTML::Lint;
use HTML::Entities; #encode_entities($_)
use URI::Escape;    #uri_escape($_)

use Image::Magick; #apparentemente parte del pacchetto libimage-size-perl 
use Image::Size;

use Net::SMTP;
use DateTime;
use DateTime::Format::Mail;


my $smtp = Net::SMTP->new('smtp.studenti.math.unipd.it'
   ,                      Hello => 'studenti.math.unipd.it'
   ,                      Timeout => 30
   ,                      Debug => 1,
    );

$smtp->mail($ENV{USER} . "\@studenti.math.unipd.it");
$smtp->to  ($ENV{USER} . "\@studenti.math.unipd.it");
$smtp->data()          ;

my $dt = DateTime->from_epoch     ( epoch => time() ) ;
#        DateTime->now; # same as ( epoch => time() )

$smtp->datasend("Date: " . DateTime::Format::Mail->format_datetime( $dt ) . "\n") ; #al posto di gmtime(time) 
$smtp->datasend("Subject: prova dello script " . $0 . " " . $$ . "\n");
$smtp->datasend("From: " . $ENV{USER} . "-noreply\@studenti.math.unipd.it\n");
$smtp->datasend("To:  \"me stesso\" <" . $ENV{USER} . "\@studenti.math.unipd.it>\n");
$smtp->datasend("\n");


my $redirect=0;
if ( $redirect ) {
    print "Status: 302 Moved\r\nLocation: perltestCARP.pl\r\n\r\n";
    $smtp->datasend(	"Lo script ha solo ridiretto il browser...\n"	);
}
else  {
    print "Content-type: text/html\r\n\r\n";

    print "Hello world!<br />\r\nThis is not really html but " . `id` .  ".<br />\r\n";
    for (my $i=0; $i<10; $i++)
    {
        print $i."<br />";
    }
    $smtp->datasend("Lo script ha stampato l'output di un ciclo...\n");
}


$smtp->dataend();
$smtp->quit;