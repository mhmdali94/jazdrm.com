<?php
/**
 * Minimal dependency-free SMTP client (STARTTLS + AUTH LOGIN), written directly
 * for this project instead of pulling in a third-party mail library.
 *
 * Talks raw SMTP over a TLS socket - no Composer, no vendor code.
 */

function smtp_read_response($socket) {
    $data = '';
    while (!feof($socket)) {
        $line = fgets($socket, 515);
        if ($line === false) {
            break;
        }
        $data .= $line;
        // A response is complete once a line has a space (not '-') as its 4th character.
        if (strlen($line) >= 4 && $line[3] === ' ') {
            break;
        }
    }
    return $data;
}

function smtp_command($socket, $command) {
    fwrite($socket, $command . "\r\n");
    return smtp_read_response($socket);
}

function smtp_code($response) {
    return (int) substr($response, 0, 3);
}

/**
 * Sends one email via an authenticated Gmail (or any STARTTLS) SMTP relay.
 *
 * @param string $to            Recipient address.
 * @param string $subject       Plain subject (UTF-8), encoded internally.
 * @param string $headersExtra  Extra RFC822 headers, each ending in "\r\n" (e.g. Reply-To, MIME-Version, Content-Type).
 * @param string $body          Full message body (already MIME-formatted if there's an attachment).
 * @param array  $smtp          ['host','port','user','pass','from_email','from_name']
 * @return array ['ok' => bool, 'error' => string|null]
 */
function smtp_send_mail($to, $subject, $headersExtra, $body, array $smtp) {
    $errno = 0;
    $errstr = '';
    $socket = @stream_socket_client(
        "tcp://{$smtp['host']}:{$smtp['port']}",
        $errno,
        $errstr,
        15
    );
    if (!$socket) {
        return ['ok' => false, 'error' => "connect failed: $errstr ($errno)"];
    }
    stream_set_timeout($socket, 15);

    $fail = function ($step, $response) use ($socket) {
        fclose($socket);
        return ['ok' => false, 'error' => "$step failed: " . trim($response)];
    };

    $banner = smtp_read_response($socket);
    if (smtp_code($banner) !== 220) {
        return $fail('connect', $banner);
    }

    $ehloDomain = $smtp['ehlo_domain'] ?? 'localhost';

    $resp = smtp_command($socket, "EHLO {$ehloDomain}");
    if (smtp_code($resp) !== 250) {
        return $fail('EHLO', $resp);
    }

    $resp = smtp_command($socket, "STARTTLS");
    if (smtp_code($resp) !== 220) {
        return $fail('STARTTLS', $resp);
    }

    if (!@stream_socket_enable_crypto($socket, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)) {
        fclose($socket);
        return ['ok' => false, 'error' => 'TLS negotiation failed'];
    }

    $resp = smtp_command($socket, "EHLO {$ehloDomain}");
    if (smtp_code($resp) !== 250) {
        return $fail('EHLO (post-TLS)', $resp);
    }

    $resp = smtp_command($socket, "AUTH LOGIN");
    if (smtp_code($resp) !== 334) {
        return $fail('AUTH LOGIN', $resp);
    }

    $resp = smtp_command($socket, base64_encode($smtp['user']));
    if (smtp_code($resp) !== 334) {
        return $fail('AUTH username', $resp);
    }

    $resp = smtp_command($socket, base64_encode($smtp['pass']));
    if (smtp_code($resp) !== 235) {
        return $fail('AUTH password', $resp);
    }

    $resp = smtp_command($socket, "MAIL FROM: <{$smtp['from_email']}>");
    if (smtp_code($resp) !== 250) {
        return $fail('MAIL FROM', $resp);
    }

    $resp = smtp_command($socket, "RCPT TO: <{$to}>");
    if (smtp_code($resp) !== 250 && smtp_code($resp) !== 251) {
        return $fail('RCPT TO', $resp);
    }

    $resp = smtp_command($socket, "DATA");
    if (smtp_code($resp) !== 354) {
        return $fail('DATA', $resp);
    }

    $fromName = $smtp['from_name'] ?? $smtp['from_email'];
    $message = "From: {$fromName} <{$smtp['from_email']}>\r\n"
        . "To: <{$to}>\r\n"
        . "Subject: =?UTF-8?B?" . base64_encode($subject) . "?=\r\n"
        . "Date: " . date('r') . "\r\n"
        . $headersExtra
        . "\r\n"
        . $body;

    // Normalize to CRLF, then dot-stuff lines starting with "." per RFC 5321.
    $message = str_replace("\r\n", "\n", $message);
    $message = str_replace("\n", "\r\n", $message);
    $message = preg_replace('/^\./m', '..', $message);

    $resp = smtp_command($socket, $message . "\r\n.");
    $ok = smtp_code($resp) === 250;

    smtp_command($socket, "QUIT");
    fclose($socket);

    return $ok ? ['ok' => true, 'error' => null] : ['ok' => false, 'error' => "send failed: " . trim($resp)];
}
