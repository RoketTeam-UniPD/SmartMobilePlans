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
	my $node = $_[1]->findnodes('(//admin)[last()]');
	my $idref = $node->pop()->getAttribute("idref");
	$idref =~ s/(\d+)$/$1 + 1/e;
	
	return $idref; 

}

1;
