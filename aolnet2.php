#!/usr/bin/env php
<?php
$in = [STDIN];
while(stream_select($in, $out, $oob, 0)) {
   fgetc(STDIN);
}
echo "ANSNet\r\n";
echo "LOGIN";
winreadline();
echo "\r\n";
//winreadline();
echo "CONNECTED\r\n";

function winreadline()
{
	$data = "";
	$done = false;
	while (!feof(STDIN) && !$done)
	{
		$byte = fread(STDIN, 1);
		echo $byte;
		$data .= $byte;

		if ($byte == "\r")
			$done = true;

	}

	return rtrim( $data, "\r" );
}
