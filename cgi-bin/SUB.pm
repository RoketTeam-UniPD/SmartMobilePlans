#!/usr/bin/perl -w

package SUB;

use strict;
use utf8;
use warnings;

use Template;
use CGI;
use POSIX;
use CGI::Session;
use XML::LibXML;

sub closeSession {
	my $session = CGI::Session->load();
	$session->close();
	$session->delete();
	$session->flush();

	return;
}


sub validateSchema {
	my $schema = XML::LibXML::Schema->new(location => $_[0]);

	eval { $schema->validate($_[1]) };

	if (my $ex = $@) {

	  return undef;
	}

	return "";
}	


sub generateID {
	my $nodes = $_[0]->findnodes('(//*[@xml:id])[last()]');
	my $idref = $nodes->pop()->getAttribute("xml:id");
	$idref =~ s/(\d+)$/$1 + 1/e;
	
	return $idref; 

}


sub generateDate {
	return $_[0] . "-" . $_[1]  . "-" - $_[2];
}

1;
