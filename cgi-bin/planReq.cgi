#!/usr/bin/perl -w

use strict;
use utf8;
use warnings;

use CGI;
use SUB;
use CGI::Session;
use HTML::Entities;
use XML::LibXML;
use POSIX qw(strftime);
use feature qw( switch );

my $parser = XML::LibXML->new();

$parser->keep_blanks(0);
my $doc = $parser->parse_file('../data/plans.xml');

my $cgi = CGI->new();

my $operator = $cgi->param('operator');
my $payments = $cgi->param('payments');
my $title = $cgi->param('title');
$title =~ tr/a-zA-Z0-9 //dc;
my $insertdatetime = strftime "%Y-%m-%dT%H:%M:%S", localtime;
my $startdate = $cgi->param('syear') . "-" . sprintf("%02d", $cgi->param('smonth')) . "-" . sprintf("%02d",$cgi->param('sday'));
my $enddate = $cgi->param('eyear') . "-" . sprintf("%02d", $cgi->param('emonth')) . "-" . sprintf($cgi->param('eday'));
my $price = $cgi->param('price');
$price =~ s/[^\d.,]//g; $price = encode_entities($price);
my $currency = $cgi->param('currency');
my $unit = $cgi->param('unit');
my $expiry = $cgi->param('expiry');
$expiry =~ s/[^\d]//g;
my $minutes = $cgi->param('minutes');
my $messages = $cgi->param('messages');
my $datasize = $cgi->param('datasize');
my $internet = $cgi->param('internet');
my $description = $cgi->param('description');

if ($title eq '' || $price eq '' || $expiry eq '' || $minutes eq '' || $messages eq '' || $internet eq '' || $description eq '') {
	saveformData();
	print $cgi->redirect('admin.cgi?e=plan-empty');  
	exit;
}

my $plan = $doc->findnodes("//" . $operator . "[title='" . $title . "']");
if ($plan) {
	saveformData();
	print $cgi->redirect('admin.cgi?e=plan-exists'); 
	exit;
}

$minutes = encode_entities($minutes);
$messages = encode_entities($messages);
$datasize = encode_entities($datasize);
$internet = encode_entities($internet);
$description = encode_entities($description);

sub saveformData {
	my $session = CGI::Session->load();

	my %formData = (
		title 		=> $title, 
		operator 	=> $operator,
		payments 	=> $payments,
		syear 		=> $cgi->param('syear'),
		smonth 		=> $cgi->param('smonth'),
		sday 		=> $cgi->param('sday'),
		eyear 		=> $cgi->param('eyear'),
		emonth 		=> $cgi->param('emonth'),
		eday 		=> $cgi->param('eday'),
		price 		=> $price,
		currency 	=> $currency,
		unit 		=> $unit,
		expiry 		=> $expiry,
		minutes     => $minutes,
		messages    => $messages,
		datasize    => $datasize,
		internet    => $internet,
		description => $description
	);
	$session->param("form-data", \%formData);
}


my $plans  = $doc->getDocumentElement;

my $title_n = XML::LibXML::Element->new('title');
$title_n->appendText($title);

my $insertdatetime_n = XML::LibXML::Element->new('insertdatetime');
$insertdatetime_n->appendText($insertdatetime);

my $available_n = XML::LibXML::Element->new('available');
my $startdate_n = XML::LibXML::Element->new('startdate');
$startdate_n->appendText($startdate);
my $enddate_n = XML::LibXML::Element->new('enddate');
$enddate_n->appendText($enddate);
$available_n->addChild($startdate_n);
$available_n->addChild($enddate_n);

my $price_n = XML::LibXML::Element->new('price');
$price_n->setAttribute('currency', $currency);
$price_n->appendText($price);

my $expiry_n = XML::LibXML::Element->new('expiry');
$expiry_n->setAttribute('unit', $unit);
$expiry_n->appendText($expiry);

my $rates_n = XML::LibXML::Element->new('rates');
my $minutes_n = XML::LibXML::Element->new('minutes');
$minutes_n->appendText($minutes);
my $messages_n = XML::LibXML::Element->new('messages');
$messages_n->appendText($messages);
my $internet_n = XML::LibXML::Element->new('internet');
$internet_n->setAttribute('datasize', $datasize);
$internet_n->appendText($internet);
$rates_n->addChild($minutes_n);
$rates_n->addChild($messages_n);
$rates_n->addChild($internet_n);

my $description_n = XML::LibXML::Element->new('description');
$description_n->appendText($description);

my $operator_n;

if ($operator eq "vodafone") {
	$operator_n = XML::LibXML::Element->new('vodafone'); 
} elsif ($operator eq "wind") { 
	$operator_n = XML::LibXML::Element->new('wind'); 
} elsif ($operator eq "tim")	{ 
	$operator_n = XML::LibXML::Element->new('tim'); 
} elsif ($operator eq "tre") { 
	$operator_n = XML::LibXML::Element->new('tre'); 
}

$operator_n->setAttribute("payments", $payments);
$operator_n->setAttribute("xml:id", SUB::generateID($doc));

$operator_n->addChild($title_n);
$operator_n->addChild($insertdatetime_n);
$operator_n->addChild($available_n);
$operator_n->addChild($price_n);
$operator_n->addChild($expiry_n);
$operator_n->addChild($rates_n);
$operator_n->addChild($description_n);

$plans->addChild($operator_n);

my $session = CGI::Session->load();
$session->clear("form-data");

$doc->toFile('../data/plans.xml', 1);
print $cgi->redirect('admin.cgi?e=plan-success');
