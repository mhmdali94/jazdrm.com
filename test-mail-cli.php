<?php
/**
 * CLI-only diagnostic: sends one test email and prints the full raw SMTP
 * conversation so delivery problems are visible directly in the terminal.
 *
 * Run on the server via SSH: php test-mail-cli.php you@example.com
 * Refuses to run over HTTP - CLI only.
 */

if (php_sapi_name() !== 'cli') {
    http_response_code(403);
    exit('CLI only.');
}

require __DIR__ . '/smtp-mailer.php';
$smtp = require __DIR__ . '/mail-config.php';

$to = $argv[1] ?? 'mhmdali94@gmail.com';

echo "Config loaded:\n";
echo "  host: {$smtp['host']}\n";
echo "  port: {$smtp['port']}\n";
echo "  user: {$smtp['user']}\n";
echo "  pass: " . str_repeat('*', max(0, strlen($smtp['pass']) - 4)) . substr($smtp['pass'], -4) . " (length " . strlen($smtp['pass']) . ")\n";
echo "  from_email: {$smtp['from_email']}\n";
echo "  sending to: {$to}\n\n";

// Verbose variant of smtp_send_mail() - identical logic, but echoes every
// command sent and every response received.
function smtp_send_mail_verbose($to, $subject, $headersExtra, $body, array $smtp) {
    $errno = 0;
    $errstr = '';
    echo ">> connecting to tcp://{$smtp['host']}:{$smtp['port']} ...\n";
    $socket = @stream_socket_client("tcp://{$smtp['host']}:{$smtp['port']}", $errno, $errstr, 15);
    if (!$socket) {
        echo "!! connect failed: $errstr ($errno)\n";
        return false;
    }
    stream_set_timeout($socket, 15);

    $read = function () use ($socket) {
        $data = smtp_read_response($socket);
        echo "<< " . trim($data) . "\n";
        return $data;
    };
    $send = function ($cmd, $label = null) use ($socket, $read) {
        echo ">> " . ($label ?? $cmd) . "\n";
        fwrite($socket, $cmd . "\r\n");
        return $read();
    };

    $banner = $read();
    if (smtp_code($banner) !== 220) { fclose($socket); return false; }

    $ehlo = $smtp['ehlo_domain'] ?? 'localhost';
    if (smtp_code($send("EHLO {$ehlo}")) !== 250) { fclose($socket); return false; }
    if (smtp_code($send("STARTTLS")) !== 220) { fclose($socket); return false; }

    echo ">> enabling TLS...\n";
    if (!@stream_socket_enable_crypto($socket, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)) {
        echo "!! TLS negotiation failed\n";
        fclose($socket);
        return false;
    }
    echo "<< TLS OK\n";

    if (smtp_code($send("EHLO {$ehlo}")) !== 250) { fclose($socket); return false; }
    if (smtp_code($send("AUTH LOGIN")) !== 334) { fclose($socket); return false; }
    if (smtp_code($send(base64_encode($smtp['user']), "[base64 username]")) !== 334) { fclose($socket); return false; }
    if (smtp_code($send(base64_encode($smtp['pass']), "[base64 password]")) !== 235) { fclose($socket); return false; }

    if (smtp_code($send("MAIL FROM: <{$smtp['from_email']}>")) !== 250) { fclose($socket); return false; }

    $rcpt = $send("RCPT TO: <{$to}>");
    if (smtp_code($rcpt) !== 250 && smtp_code($rcpt) !== 251) { fclose($socket); return false; }

    if (smtp_code($send("DATA")) !== 354) { fclose($socket); return false; }

    $fromName = $smtp['from_name'] ?? $smtp['from_email'];
    $message = "From: {$fromName} <{$smtp['from_email']}>\r\n"
        . "To: <{$to}>\r\n"
        . "Subject: =?UTF-8?B?" . base64_encode($subject) . "?=\r\n"
        . "Date: " . date('r') . "\r\n"
        . $headersExtra
        . "\r\n"
        . $body;
    $message = str_replace("\r\n", "\n", $message);
    $message = str_replace("\n", "\r\n", $message);
    $message = preg_replace('/^\./m', '..', $message);

    echo ">> [DATA payload, " . strlen($message) . " bytes]\n";
    $resp = $send($message . "\r\n.", "[end of DATA: CRLF . CRLF]");
    $ok = smtp_code($resp) === 250;

    $send("QUIT");
    fclose($socket);
    return $ok;
}

$ok = smtp_send_mail_verbose(
    $to,
    'CLI test email - jazdrm.com',
    "MIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\n",
    "This is a CLI test from test-mail-cli.php, sent at " . date('Y-m-d H:i:s') . ".\n",
    $smtp
);

echo "\nResult: " . ($ok ? "OK (accepted with 250)" : "FAILED") . "\n";
