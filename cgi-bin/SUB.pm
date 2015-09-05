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





# stramite la avriabile $title viene recepito il titolo da assegnale alla pagina
sub printHeader {
	my ($title) = @_;
	my $hr = qq{<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html lang="en" xml:lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
	<title>$title - Smart Mobile Plans</title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
	<meta name="keywords" content=""/>
	<meta name="viewport" content="width=device-width, initial-scale=1"/>
	<link rel="stylesheet" type="text/css" href="../../css/main.css" media="all"/>
	<link href="http://fonts.googleapis.com/css?family=Open+Sans:400,700" rel="stylesheet" type="text/css"/>
</head>
<body>
};
	return $hr;
}




sub printHeaderSITE {
	my $hr = qq{
	<!-- Start Header -->
	<div class="header">
		<h1>Smart Mobile Plans</h1>
		<h2>Choosing a mobile phone plan has never been this simple!</h2>
	</div> <!-- End Header -->
};
	return $hr;
}





sub printMenuSITE {
	my ($active) = @_;
	my $hr = qq{
	<!-- Start Menu -->
	<div class="menu">
		<ul>
	};

	if(lc $active eq lc 'home'){
		$hr .= qq{		<li><a class="active" href="#" title="Home">HOME</a></li>
	};
	}else{
		$hr .= qq{		<li><a href="home.pl" title="Home">HOME</a></li>
	};
	}

	if(lc $active eq lc 'tim'){
		$hr .= qq{		<li><a class="active" href="#" title="TIM">TIM</a></li>
	};
	}else{
		$hr .= qq{		<li><a href="operator.cgi?name=tim">TIM</a></li>
	};
	}

	if(lc $active eq lc 'vodafone'){
		$hr .= qq{		<li><a class="active" href="#" title="VODAFONE">VODAFONE</a></li>
	};
	}else{
		$hr .= qq{		<li><a href="operator.cgi?name=vodafone">VODAFONE</a></li>
	};
	}

	if(lc $active eq lc 'tre'){
		$hr .= qq{		<li><a class="active" href="#" title="TRE">TRE</a></li>
	};
	}else{
		$hr .= qq{		<li><a href="operator.cgi?name=tre">TRE</a></li>
	};
	}

	if(lc $active eq lc 'wind'){
		$hr .= qq{		<li><a class="active" href="#" title="WIND">WIND</a></li>
	};
	}else{
		$hr .= qq{		<li><a href="operator.cgi?name=wind">WIND</a></li>
	};
	}

	$hr .= qq{	</ul>
	</div> <!-- End Menu -->
	};

	return $hr;
}





sub printBreadcrumbsSITE {

	my @array = @{_};

	my $hr = qq{
	<div class="breadcrumbs">
		<p>You are in:
	};

	my $size = scalar @{ $array[0] };
	my $i = 1;

	foreach my $desc (@{ $array[0] }) {

		if($i != $size){
			$hr .= qq{\t\t<a title="$desc->[0]" href="$desc->[1]">}.uc$desc->[0].qq{ </a>};
			$hr .= qq{\\};
		}
		$i++;
	}

	$hr .= qq{\n\t\t\t<a title="$array[0][$size-1][0]">}.uc$array[0][$size-1][0].qq{ </a>};



	$hr .= qq{
		</p>
	</div> <!-- End Breadcrumbs -->
	};




	#print $array[0][1][1], "\n";

	#print $array;
	#my $hr = qq{
	#};


	return $hr;
}










1;
