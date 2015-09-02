#!/usr/bin/perl -w

package SUB;

use strict;
use utf8;
use warnings;

use Template;
use CGI;
use CGI::Session;

sub closeSession {
	my $session = CGI::Session->load();
	$session->close();
	$session->delete();
	$session->flush();

	return;
}
