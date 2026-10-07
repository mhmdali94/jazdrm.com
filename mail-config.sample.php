<?php
/**
 * Copy this file to mail-config.php and fill in the real values there.
 * mail-config.php is gitignored - it is never committed to this public repo.
 */

return [
    'host' => 'smtp.gmail.com',
    'port' => 587,
    'user' => 'your-account@gmail.com',       // Gmail address used to authenticate and send
    'pass' => 'xxxx xxxx xxxx xxxx',          // Gmail App Password (not the normal account password)
    'from_email' => 'your-account@gmail.com', // must match 'user' for Gmail's SMTP relay
    'from_name' => 'jazdrm.com',
    'ehlo_domain' => 'jazdrm.com',
];
